# Copyright (c) 2021, Ora Lassila & So Many Aircraft
# All rights reserved.
#
# See LICENSE for licensing information
#
# This module implements XMP support for RDFLib, and provides some useful helper
# functionality for reading, writing, and manipulating XMP metadata.
#
# Some code was copied from rdflib.plugins.parsers.xmlrdf.RDFXMLHandler and subsequently
# modified because RDFLib did not provide suitable extension points. That code is
# Copyright (c) 2002-2020, RDFLib Team and is distributed under a similar 3-clause BSD
# License; see this file: https://github.com/RDFLib/rdflib/blob/master/LICENSE

from rdflib import RDF, URIRef, BNode, Literal, Namespace, Graph, plugin
from rdflib.exceptions import Error
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from rdflib.plugins.parsers.rdfxml import RDFXMLHandler, ErrorHandler
from rdflib.plugins.serializers.rdfxml import PrettyXMLSerializer
from xml.sax import make_parser, handler, SAXParseException
import io
import re
from datetime import datetime
import os.path
import pathlib
from urllib.parse import urlparse

TOOLNAME = "So Many Aircraft xmptools 0.1"
XMP_NS = "adobe:ns:meta/"
XMP_NAME = "xmpmeta"
XMP_TAG_OPEN = '<x:{0}'.format(XMP_NAME).encode('utf-8')
XMP_TAG_CLOSE = '</x:{0}>'.format(XMP_NAME).encode('utf-8')
XMP_TAG_OPEN_FULL =\
    '<x:{0} xmlns:x="{1}" x:xmptk="{2}">\n'.format(XMP_NAME, XMP_NS, TOOLNAME).encode('utf-8')

class FileTypeError(Error):
    def __init__(self, message, path, original=None):
        super().__init__(message.format(path, original))
        self.path = path
        self.original = original

class XMPHandler(RDFXMLHandler):
    def reset(self):
        super().reset()
        e = self.stack[1]
        e.start = self.envelope_element_start

    def envelope_element_start(self, name, qname, attrs):
        if name[0] == XMP_NS and name[1] == XMP_NAME:
            nxt = getattr(self, "next")
            nxt.start = self.document_element_start
            nxt.end = lambda n, qn: None
        else:
            raise FileTypeError("This is not XMP", None)

    def node_element_end(self, name, qname):
        # copied from rdflib.plugins.parsers.xmlrdf.RDFXMLHandler and
        # modified because there is now an extra element in the stack
        if self.parent.object and self.current != self.stack[3]:
            self.error("Repeated node-elements: %s" % "".join(name))
        self.parent.object = self.current.subject

class XMPParser(Parser):
    def __init__(self):
        self._parser = None
        super().__init__()

    def parse(self, source, sink, **args):
        parser = make_parser()
        parser.setFeature(handler.feature_namespaces, 1)
        xmp = XMPHandler(sink)
        xmp.setDocumentLocator(source)
        parser.setContentHandler(xmp)
        parser.setErrorHandler(ErrorHandler())
        content_handler = parser.getContentHandler()
        self._parser = parser
        preserve_bnode_ids = args.get("preserve_bnode_ids", None)
        if preserve_bnode_ids is not None:
            content_handler.preserve_bnode_ids = preserve_bnode_ids
        try:
            self._parser.parse(source)
        except SAXParseException as e:
            raise FileTypeError('Possibly not XMP because "{1}"', None, original=e)

class XMPSerializer(PrettyXMLSerializer):
    # We must subclass PrettyXMLSerializer, because the Adobe XMP toolkit expects
    # blank nodes to be serialized "in line" and not as separate Descriptions. The
    # plain XMLSerializer does not do this. :-(
    def __init__(self, store):
        super().__init__(store)
        self.xmpfile = None
        self.__serialized = None

    def serialize(self, stream, base=None, encoding=None, xmpfile=None, **args):
        self.xmpfile = URIRef(xmpfile)
        self.__serialized = {}
        stream.write(XMP_TAG_OPEN_FULL)
        xmlstream = io.BytesIO()
        super().serialize(xmlstream, base=base, encoding=encoding, **args)
        rdf = io.BytesIO(xmlstream.getvalue())
        rdf.readline()  # this is all ugly code, but we must skip the initial XML declaration
        for line in rdf.readlines():
            stream.write(line)
        stream.write(XMP_TAG_CLOSE)

    def relativize(self, uri):
        if uri == self.xmpfile:
            return URIRef("")  # this is here so we do not need to insert a misleading xml:base
        else:
            return super().relativize(uri)

    RDFLI = str(RDF) + "li"  # We cannot use RDF.li because RDF is a closed namespace

    def predicate(self, pred, obj, depth=1):
        # Replace actual container item predicates with <rdf:li> as per the XMP spec
        super().predicate(self.RDFLI if isContainerItemPredicate(pred) else pred, obj, depth)

plugin.register("xmp", Parser, "xmptools", "XMPParser")
plugin.register("xmp", Serializer, "xmptools", "XMPSerializer")

XMP = Namespace("http://ns.adobe.com/xap/1.0/")
EXIF = Namespace("http://ns.adobe.com/exif/1.0/")
CRS = Namespace("http://ns.adobe.com/camera-raw-settings/1.0/")
DC = Namespace("http://purl.org/dc/elements/1.1/")

class MoreThanOneValue(Error):
    pass

LI_MATCH_PATTERN = re.compile(str(RDF) + "_([0-9]+)")
LI_CREATE_PATTERN = str(RDF) + "_{0}"

def makeFileURI(path):
    return pathlib.Path(os.path.abspath(path)).as_uri()

def isContainerItemPredicate(uri):
    match = LI_MATCH_PATTERN.match(uri)
    return int(match.group(1)) if match else None

def makeContainerItemPredicate(index):
    return LI_CREATE_PATTERN.format(index)

def getContainerStatements(graph, source, predicate):
    if not isinstance(source, URIRef):
        source = URIRef(source)
    containers = list(graph.objects(source, predicate))
    n = len(containers)
    if n == 1:
        statements = graph.triples((containers[0], None, None))
        return [statement for statement in statements if isContainerItemPredicate(statement[1])]
    elif n == 0:
        return None
    else:
        raise MoreThanOneValue("Expected only one value for {0}".format(predicate))

def adjustNodes(node_map, source_graph, destination_graph=None, check_predicates=False):
    if destination_graph is None:
        destination_graph = type(source_graph)()
    for s, p, o in source_graph:
        for node in node_map:
            if s == node:
                s = node_map[node]
            if check_predicates and p == node:
                p = node_map[node]
            if o == node:
                o = node_map[node]
        destination_graph.add((s, p, o))
    if isinstance(destination_graph, XMPMetadata):
        destination_graph.url = node_map[source_graph.url]
        destination_graph.sourceIsXMP = False
    return destination_graph

JPEG_EXTENSIONS = [".jpg", ".jpeg", ".JPG", ".JPEG"]
TIFF_EXTENSIONS = [".tif", ".tiff", ".TIF", ".TIFF"]
DNG_EXTENSIONS  = [".dng", ".DNG"]
RAW_EXTENSIONS  = [".cr2", ".CR2", ".cr3", ".CR3"]  # obviously wholly incomplete still
XMP_EXTENSIONS  = [".xmp", ".XMP"]

class XMPMetadata(Graph):
    def __init__(self, url=None):
        self.initialized = False
        if url is None:
            self.url = None
            self.sourceIsXMP = False  # signals that content didn't come from an XMP sidecar file
            self.segment_count = 0
        else:
            self.url = URIRef(url)
            self.sourceIsXMP = True
            self.segment_count = 1
        super().__init__(identifier=self.url)
        if url is not None:
            self.read()

    @classmethod
    def fromFile(cls, path):
        # LOGIC:
        #   1) Try a corresponding XMP sidecar file
        #   2) Try the image file itself
        #   3) Nothing
        (base, extension) = os.path.splitext(path)
        xmppath = base + ".xmp"
        try:
            return cls(xmppath), xmppath
        except (FileNotFoundError, FileTypeError):
            try:
                return cls.fromImageFile(path), path
            except FileTypeError:
                return None, None

    @classmethod
    def fromImageFile(cls, path):
        (_, extension) = os.path.splitext(path)
        if extension in JPEG_EXTENSIONS:
            return cls.fromJPEG(path)
        elif extension in TIFF_EXTENSIONS or extension in DNG_EXTENSIONS:
            with open(path, "rb") as file:
                # we'll take our chances...
                return cls.attemptToReadXMP(path, file)
        elif extension in RAW_EXTENSIONS:
            raise FileTypeError("Try reading from the sidecar file of {0}", path)
        else:
            raise FileTypeError("Unrecognized file type: {0}", path)

    @classmethod
    def fromJPEG(cls, path):
        with open(path, "rb") as file:
            if file.read(3) == b"\xff\xd8\xff":
                return cls.attemptToReadXMP(path, file)
            else:
                raise FileTypeError("Not a JPEG file: {0}", path)

    @classmethod
    def attemptToReadXMP(cls, path, file):
        stuff = file.read()
        xmp = None
        j = 0
        while True:
            try:
                i = stuff.index(XMP_TAG_OPEN, j)
            except ValueError:
                return xmp
            try:
                j = stuff.index(XMP_TAG_CLOSE, i) + len(XMP_TAG_CLOSE)
            except ValueError:
                return xmp
            if xmp is None:
                xmp = cls()  # empty graph
                xmp.url = URIRef(makeFileURI(os.path.abspath(path)))
            xmp.parse(io.BytesIO(stuff[i:j]), format="xmp", publicID=makeFileURI(path))
            xmp.initialized = True
            xmp.segment_count += 1

    def read(self):
        if self.sourceIsXMP:
            self.parse(self.url, format="xmp")
            self.initialized = True
        else:
            raise NotImplementedError("Use of read() with embedded metadata is not supported")

    def write(self, destination=None):
        if destination:
            # If destination is specified, it must be a pathname ending in ".xmp", or a stream
            if isinstance(destination, str):
                if not destination.endswith(".xmp"):
                    raise ValueError("Only XMP files can be written, not " + destination)
            elif not isinstance(destination, io.IOBase):
                raise ValueError("Unsupported destination: " + destination)
        elif not self.sourceIsXMP:
            raise NotImplementedError("Cannot write metadata back to " + self.url)
        else:
            destination = self.url
        self.serialize(destination=destination, format="xmp", xmpfile=self.url)

    def getOneStatement(self, predicate):
        statements = list(self.triples((self.url, predicate, None)))
        return statements[0] if statements and len(statements) > 0 else None

    def getValue(self, predicate):
        statement = self.getOneStatement(predicate)
        return statement[2] if statement else None

    def getDate(self, predicate=XMP.MetadataDate):
        value = self.getValue(predicate)
        if value:
            date = value.value
            return datetime.fromisoformat(date) if isinstance(date, str) else date
        else:
            return None

    def setDate(self, timestamp=datetime.utcnow(), predicate=XMP.MetadataDate):
        self.set((self.url, predicate, Literal(timestamp)))

    def getContainerItems(self, predicate):
        statements = getContainerStatements(self, self.url, predicate)
        return [statement[2].value for statement in statements] if statements else None

    def setContainerItems(self, predicate, values, newtype=RDF.Seq):
        # Having to write code like this is a clear indication that triples are the wrong
        # abstraction for graphs, way too low level. Just sayin'.
        if values and len(values) > 0:
            statements = getContainerStatements(self, self.url, predicate)
            if statements:
                container = statements[0][0]
                for statement in statements:
                    self.remove(statement)
            else:
                container = BNode()
                self.add((self.url, predicate, container))
                self.add((container, RDF.type, newtype))
            i = 1
            for value in values:
                self.add((container, URIRef(makeContainerItemPredicate(i)), Literal(value)))
                i += 1
        else:
            statement = self.getOneStatement(predicate)
            container = statement[2]
            self.remove((self.url, predicate, container))
            self.remove((container, None, None))

    def container2repeated(self, predicate):
        # We understand that this messes with ordering
        items = self.getContainerItems(predicate)
        if items:
            self.setContainerItems(predicate, [])
            for item in items:
                self.add((self.url, predicate, item))

    def repeated2container(self, predicate, newtype=RDF.Seq):
        # We understand that this messes with ordering
        statements = self.triples((self.url, predicate, None))
        if statements:
            for statement in statements:
                self.remove(statement)
            self.setContainerItems(predicate, [o for _, _, o in statements], newtype=newtype)

    def adjustImageURI(self, new_extension=None):
        # Logic:
        #   1. If no new extension specified, use crs:RawFileName value for the new extension
        #      - if no RawFileName found, signal an error
        #   2. Otherwise, replace old extension with the new extension provided
        original = self.getValue(CRS.RawFileName)
        if new_extension is None:
            if original is None:
                raise FileTypeError("No new extension specified for {0}", self.url)
            else:
                url = urlparse(str(self.url))
                path, ext = os.path.splitext(url.path)
                _, new_extension = os.path.splitext(str(original))
                new_uri = url._replace(path=(path + new_extension)).geturl()
        else:
            base, _ = os.path.splitext(str(self.url))
            new_uri = base + new_extension
        return adjustNodes({self.url: URIRef(new_uri)}, self)
