from rdflib.store import Store


class Memory2(Store):
    """\
    An in memory implementation of a triple store.

    Same as Memory1 above, but is Context-aware, Graph-aware, and Formula-aware
    Authors: Ashley Sommer
    """

    context_aware = True
    formula_aware = True
    graph_aware = True

    def __init__(self, configuration=None, identifier=None):
        super(Memory2, self).__init__(configuration)
        self.identifier = identifier

        # indexed by [subject][predicate][object]
        self.__spo = {}

        # indexed by [predicate][object][subject]
        self.__pos = {}

        # indexed by [predicate][object][subject]
        self.__osp = {}

        self.__namespace = {}
        self.__prefix = {}
        self.__context_obj_map = {}
        self.__tripleContexts = {}
        self.__contextTriples = {None: set()}
        # all contexts used in store (unencoded)
        self.__all_contexts = set()
        # default context information for triples
        self.__defaultContexts = None

    def add(self, triple, context, quoted=False):
        """\
        Add a triple to the store of triples.
        """
        # add dictionary entries for spo[s][p][p] = 1 and pos[p][o][s]
        # = 1, creating the nested dictionaries where they do not yet
        # exits.
        Store.add(self, triple, context, quoted=quoted)
        if context is not None:
            self.__all_contexts.add(context)
        subject, predicate, object_ = triple
        self.__add_triple_context(triple, context, quoted)

        spo = self.__spo
        try:
            po = spo[subject]
        except LookupError:
            po = spo[subject] = {}
        try:
            o = po[predicate]
        except LookupError:
            o = po[predicate] = {}
        o[object_] = 1

        pos = self.__pos
        try:
            os = pos[predicate]
        except LookupError:
            os = pos[predicate] = {}
        try:
            s = os[object_]
        except LookupError:
            s = os[object_] = {}
        s[subject] = 1

        osp = self.__osp
        try:
            sp = osp[object_]
        except LookupError:
            sp = osp[object_] = {}
        try:
            p = sp[subject]
        except LookupError:
            p = sp[subject] = {}
        p[predicate] = 1

    def remove(self, triple_pattern, context=None):
        req_ctx = self.__ctx_to_str(context)
        for triple, c in self.triples(triple_pattern, context=context):
            subject, predicate, object_ = triple
            for ctx in self.__get_context_for_triple(triple):
                if context is not None and req_ctx != ctx:
                    continue
                self.__remove_triple_context(triple, ctx)
            ctxs = self.__get_context_for_triple(triple, skipQuoted=True)
            if None in ctxs and (context is None or len(ctxs) == 1):
                # remove from default graph too
                self.__remove_triple_context(triple, None)
            if len(self.__get_context_for_triple(triple)) == 0:
                del self.__spo[subject][predicate][object_]
                del self.__pos[predicate][object_][subject]
                del self.__osp[object_][subject][predicate]
                del self.__tripleContexts[triple]
        if req_ctx is not None and req_ctx in self.__contextTriples and len(self.__contextTriples[req_ctx]) == 0:
            # all triples are removed out of this context
            # and it's not the default context so delete it
            del self.__contextTriples[req_ctx]

        if triple_pattern == (None, None, None) and context in self.__all_contexts and not self.graph_aware:
            # remove the whole context
            self.__all_contexts.remove(context)

    def triples(self, triple_pattern, context=None):
        """A generator over all the triples matching"""
        req_ctx = self.__ctx_to_str(context)
        subject, predicate, object_ = triple_pattern

        # all triples case (no triple parts given as pattern)
        if subject is None and predicate is None and object_ is None:
            # Just dump all known triples from the given graph
            if req_ctx not in self.__contextTriples:
                return
            for triple in self.__contextTriples[req_ctx].copy():
                yield triple, self.__contexts(triple)

        # optimize "triple in graph" case (all parts given)
        elif subject is not None and predicate is not None and object_ is not None:
            triple = triple_pattern
            try:
                _ = self.__spo[subject][predicate][object_]
                if self.__triple_has_context(triple, req_ctx):
                    yield triple, self.__contexts(triple)
            except KeyError:
                return

        elif subject is not None:  # subject is given
            spo = self.__spo
            if subject in spo:
                subjectDictionary = spo[subject]
                if predicate is not None:  # subject+predicate is given
                    if predicate in subjectDictionary:
                        if object_ is not None:  # subject+predicate+object is given
                            if object_ in subjectDictionary[predicate]:
                                triple = (subject, predicate, object_)
                                if self.__triple_has_context(triple, req_ctx):
                                    yield triple, self.__contexts(triple)
                            else:  # given object not found
                                pass
                        else:  # subject+predicate is given, object unbound
                            for o in list(subjectDictionary[predicate].keys()):
                                triple = (subject, predicate, o)
                                if self.__triple_has_context(triple, req_ctx):
                                    yield triple, self.__contexts(triple)
                    else:  # given predicate not found
                        pass
                else:  # subject given, predicate unbound
                    for p in list(subjectDictionary.keys()):
                        if object_ is not None:  # object is given
                            if object_ in subjectDictionary[p]:
                                triple = (subject, p, object_)
                                if self.__triple_has_context(triple, req_ctx):
                                    yield triple, self.__contexts(triple)
                            else:  # given object not found
                                pass
                        else:  # object unbound
                            for o in list(subjectDictionary[p].keys()):
                                triple = (subject, p, o)
                                if self.__triple_has_context(triple, req_ctx):
                                    yield triple, self.__contexts(triple)
            else:  # given subject not found
                pass
        elif predicate is not None:  # predicate is given, subject unbound
            pos = self.__pos
            if predicate in pos:
                predicateDictionary = pos[predicate]
                if object_ is not None:  # predicate+object is given, subject unbound
                    if object_ in predicateDictionary:
                        for s in list(predicateDictionary[object_].keys()):
                            triple = (s, predicate, object_)
                            if self.__triple_has_context(triple, req_ctx):
                                yield triple, self.__contexts(triple)
                    else:  # given object not found
                        pass
                else:  # predicate is given, object+subject unbound
                    for o in list(predicateDictionary.keys()):
                        for s in list(predicateDictionary[o].keys()):
                            triple = (s, predicate, o)
                            if self.__triple_has_context(triple, req_ctx):
                                yield triple, self.__contexts(triple)
        elif object_ is not None:  # object is given, subject+predicate unbound
            osp = self.__osp
            if object_ in osp:
                objectDictionary = osp[object_]
                for s in list(objectDictionary.keys()):
                    for p in list(objectDictionary[s].keys()):
                        triple = (s, p, object_)
                        if self.__triple_has_context(triple, req_ctx):
                            yield triple, self.__contexts(triple)
        else:  # subject+predicate+object unbound
            # Shouldn't get here if all other cases above worked correctly.
            spo = self.__spo
            for s in list(spo.keys()):
                subjectDictionary = spo[s]
                for p in list(subjectDictionary.keys()):
                    for o in list(subjectDictionary[p].keys()):
                        triple = (s, p, o)
                        if self.__triple_has_context(triple, req_ctx):
                            yield triple, self.__contexts(triple)

    def bind(self, prefix, namespace):
        self.__prefix[namespace] = prefix
        self.__namespace[prefix] = namespace

    def namespace(self, prefix):
        return self.__namespace.get(prefix, None)

    def prefix(self, namespace):
        return self.__prefix.get(namespace, None)

    def namespaces(self):
        for prefix, namespace in self.__namespace.items():
            yield prefix, namespace

    def contexts(self, triple=None):
        if triple is None or triple == (None, None, None):
            return (context for context in self.__all_contexts)

        subj, pred, obj = triple
        try:
            _ = self.__spo[subj][pred][obj]
            return self.__contexts(triple)
        except KeyError:
            return (_ for _ in [])

    def __len__(self, context=None):
        ctx = self.__ctx_to_str(context)
        if ctx not in self.__contextTriples:
            return 0
        return len(self.__contextTriples[ctx])

    def add_graph(self, graph):
        if not self.graph_aware:
            Store.add_graph(self, graph)
        else:
            self.__all_contexts.add(graph)

    def remove_graph(self, graph):
        if not self.graph_aware:
            Store.remove_graph(self, graph)
        else:
            self.remove((None, None, None), graph)
            try:
                self.__all_contexts.remove(graph)
            except KeyError:
                pass  # we didn't know this graph, no problem

    # internal utility methods below
    def __add_triple_context(self, triple, context, quoted):
        """add the given context to the set of contexts for the triple"""
        ctx = self.__ctx_to_str(context)
        quoted = bool(quoted)
        try:
            subj, pred, obj = triple
            _ = self.__spo[subj][pred][obj]
            # we know the triple exists somewhere in the store
            if triple not in self.__tripleContexts:
                # triple exists with default ctx info
                # start with a copy of the default ctx info
                self.__tripleContexts[triple] = self.__defaultContexts.copy()

            self.__tripleContexts[triple][ctx] = quoted
            if not quoted:
                self.__tripleContexts[triple][None] = quoted
        except KeyError:
            # the triple didn't exist before in the store
            if quoted:  # this context only
                self.__tripleContexts[triple] = {ctx: quoted}
            else:  # default context as well
                self.__tripleContexts[triple] = {ctx: quoted, None: quoted}

        # if the triple is not quoted add it to the default context
        if not quoted:
            self.__contextTriples[None].add(triple)

        # always add the triple to given context, making sure it's initialized
        if ctx not in self.__contextTriples:
            self.__contextTriples[ctx] = set()
        self.__contextTriples[ctx].add(triple)

        # if this is the first ever triple in the store, set default ctx info
        if self.__defaultContexts is None:
            self.__defaultContexts = self.__tripleContexts[triple]

        # if the context info is the same as default, no need to store it
        if self.__tripleContexts[triple] == self.__defaultContexts:
            del self.__tripleContexts[triple]

    def __get_context_for_triple(self, triple, skipQuoted=False):
        """return a list of contexts (str) for the triple, skipping
        quoted contexts if skipQuoted==True"""

        ctxs = self.__tripleContexts.get(triple, self.__defaultContexts)

        if not skipQuoted:
            return ctxs.keys()

        return [ctx for ctx, quoted in ctxs.items() if not quoted]

    def __triple_has_context(self, triple, ctx):
        """return True if the triple exists in the given context"""
        return ctx in self.__tripleContexts.get(triple, self.__defaultContexts)

    def __remove_triple_context(self, triple, ctx):
        """remove the context from the triple"""
        ctxs = self.__tripleContexts.get(triple, self.__defaultContexts).copy()
        del ctxs[ctx]
        if ctxs == self.__defaultContexts:
            del self.__tripleContexts[triple]
        else:
            self.__tripleContexts[triple] = ctxs
        self.__contextTriples[ctx].remove(triple)

    def __ctx_to_str(self, ctx):
        if ctx is None:
            return None
        try:
            # ctx could be a graph. In that case, use its identifier
            ctx_str = "{}:{}".format(str(ctx.identifier.__class__.__name__), str(ctx.identifier))
            self.__context_obj_map[ctx_str] = ctx
            return ctx_str
        except AttributeError:
            # otherwise, ctx should be a URIRef or BNode or str
            if isinstance(ctx, str):
                ctx_str = "{}:{}".format(str(ctx.__class__.__name__), str(ctx))
                if ctx_str in self.__context_obj_map:
                    return ctx_str
                self.__context_obj_map[ctx_str] = ctx
                return ctx_str
            raise RuntimeError("Cannot use that type of object as a Graph context")

    def __contexts(self, triple):
        """return a generator for all the non-quoted contexts
        (dereferenced) the encoded triple appears in"""
        return (
            self.__context_obj_map.get(ctx_str, ctx_str)
            for ctx_str in self.__get_context_for_triple(triple, skipQuoted=True)
            if ctx_str is not None
        )
