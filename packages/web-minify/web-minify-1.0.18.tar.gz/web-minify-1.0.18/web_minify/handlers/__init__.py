import importlib
import pkgutil

import logging


logger = logging.getLogger(__name__)


class HandlerManager:
    def __init__(self):
        self.handler_extensions = []
        self.handler_names = []
        self.handler_classes = []
        self.handlers_by_name = {}
        self.handlers_by_extension = {}
        self._enumerate_handlers()

    def _enumerate_handlers(self):
        self.handlers = {}
        for importer, modname, is_package in pkgutil.iter_modules(__path__):
            imported_mod = importlib.import_module(f"web_minify.handlers.{modname}")
            if not imported_mod:
                logger.warning(f"Could not import module '{modname}', skipping...")
                continue
            handler_class = getattr(imported_mod, "Handler")
            if not handler_class:
                logger.warning(f"Could not find Handler class for '{modname}', skipping...")
                continue
            if not isinstance(handler_class, type):
                logger.warning(f"Handler symbol is not class for '{modname}', skipping...")
                continue
            handler_extensions = handler_class.extensions()
            if not handler_extensions:
                logger.warning(f"Handler does not support any extensions for '{modname}', skipping...")
                continue
            handler_name = handler_class.name()
            self.handler_classes.append(handler_class)
            self.handler_names.append(handler_name)
            self.handler_extensions.extend(handler_extensions)

    def prepare_handlers(self, settings):
        self.handlers = {}
        for handler_class in self.handler_classes:
            handler = handler_class(settings)
            if not handler:
                logger.warning(f"Could not instanciate handler for '{handler_class.name()}', skipping...")
                continue
            self.handlers_by_name[handler.name()] = handler
            for extension in handler.extensions():
                # logger.warning(f"Configuring handler {name} for .{extension}")
                self.handlers_by_extension[extension] = handler

    def get_handler_by_extension(self, extension):
        return self.handlers_by_extension.get(extension, None)

    def get_handler_by_name(self, name):
        return self.handlers_by_name.get(name, None)

    def get_supported_extensions(self):
        return self.handler_extensions

    def get_handler_names(self):
        return self.handler_names
