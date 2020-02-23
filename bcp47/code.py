

class BCP47Code(object):
    _errors = None
    _lang_code = None
    tag_parts = (
        "language",
        "extlang",
        "script",
        "region",
        "variant")

    def __init__(self, bcp47, *args, **kwargs):
        self.bcp47 = bcp47
        self.kwargs = {}
        args = (
            args[0].split("-") + list(args[1:])
            if args and ("-" in args[0])
            else args)
        self.construct(*args, **kwargs)

    def __repr__(self):
        return (
            "<%s.%s '%s' />"
            % (self.__module__,
               self.__class__.__name__,
               self.lang_code))

    def __str__(self):
        return self.lang_code

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def extlang(self):
        return self.kwargs.get("extlang")

    @property
    def grandfathered(self):
        return self.kwargs.get("grandfathered")

    @property
    def language(self):
        return self.kwargs.get("language")

    @property
    def region(self):
        return self.kwargs.get("region")

    @property
    def script(self):
        return self.kwargs.get("script")

    @property
    def variant(self):
        return self.kwargs.get("variant")

    def construct(self, *args, **kwargs):
        if args and kwargs:
            raise Exception(
                "Mixture of args and kwargs, "
                "use one or the other when constructing language codes")
        elif not (args or kwargs):
            raise Exception(
                "No arguments provided to construct a language code")
        if args:
            return self.construct_from_args(*args)
        return self.construct_from_kwargs(**kwargs)

    def _add_prefix(self, parts, args):
        language = self.bcp47["languages"].get(args[0])
        if language:
            self.kwargs["language"] = args[0]
            parts.append(args[0])
            return
        if not self.bcp47["grandfathereds"].get(args[0]):
            raise Exception(
                "Language '%s' not recognized"
                % (args[0]))
        self.kwargs["grandfathered"] = args[0]
        parts.append(args[0])
        if args[1:]:
            raise Exception(
                "Grandfathered tags cannot have "
                "further extensions - found '%s'"
                % args[1:])

    def _maybe_add_part(self, parts, tag_types, part):
        for part_type in tag_types:
            _part = self.bcp47["%ss" % part_type].get(part)
            if _part:
                # probs need some specific code here
                # for backchecking allowed prefixes etc
                tag_types = tag_types[tag_types.index(part_type):]
                parts.append(part)
                self.kwargs[part_type] = part
                return _part

    def construct_from_args(self, *args):
        parts = []
        self._add_prefix(parts, args)
        args = args[1:]
        if not args:
            self._lang_code = "-".join(parts)
            return
        tag_types = self.tag_parts[1:]
        for part in args:
            if not tag_types:
                raise Exception(
                    "Unrecognized tag part '%s'" % part)
            if not self._maybe_add_part(parts, tag_types, part):
                raise Exception(
                    "Unrecognized tag part '%s'" % (part))
        self._lang_code = "-".join(parts)

    def _add_part(self, parts, part_type, name):
        if not name:
            return
        if name not in self.bcp47["%ss" % part_type]:
            raise Exception(
                "%s '%s' not recognized"
                % (part_type.capitalize(), name))
        parts.append(name)

    def construct_from_kwargs(self, **kwargs):
        grandfathered = kwargs.get("grandfathered")
        language = kwargs.get("language")
        parts = []

        if grandfathered and language:
            raise Exception(
                "You can only specify one of grandfathered or language. "
                "You passed %s" % ((grandfathered, language), ))
        if not (grandfathered or language):
            raise Exception(
                "You must specify one of grandfathered or language")
        for part in self.tag_parts:
            if grandfathered and part == "language":
                self._add_part(parts, "grandfathered", kwargs.get(part))
                break
            self._add_part(parts, part, kwargs.get(part))
        self.kwargs = kwargs
        self._lang_code = "-".join(parts)
