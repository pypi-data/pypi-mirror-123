from typing import Union

from .utils import todict


class Component:
    type: int
    custom_id: str
    disabled: bool

    def __init__(self, type: int, disabled: bool = False, id: str = None, **kwargs):
        self.type = type
        self.custom_id = id
        self.disabled = disabled if disabled else None
        for k,v in kwargs.items():
            self.__setattr__(k,v)


    @property
    def dict(self):
        return todict(self)


class Button(Component):
    label: str
    emoji: dict
    url: str
    style: int

    def __init__(self, label: str, style:int, id: str, emoji: dict = None, url: str = None, disabled: bool = False):
        super().__init__(2, disabled, id)

        self.label = label
        self.emoji = emoji
        self.url = url
        self.style = style


class SelectOption:
    label:str
    value:str
    description:str
    emoji:dict
    default:bool

    def __init__(self, label:str, value:str, description:str = None, emoji:dict = None, default:bool = None):
        self.default = default
        self.emoji = emoji
        self.description = description
        self.value = value
        self.label = label

    @property
    def dict(self):
        return todict(self)


class SelectMenu(Component):
    options: [SelectOption]
    placeholder: str
    min_values: int
    max_values: int

    def __init__(self, id:str, options:[Union[SelectOption,str]] = None, placeholder:str = None, min_values:int = None, max_values:int = None, disabled: bool = False):
        super().__init__(3, disabled, id)
        self.max_values = max_values
        self.min_values = min_values
        self.placeholder = placeholder
        if options[0] is SelectOption:
            self.options = options
        elif options[0] is str:
            self.options = []
            for i in options:
                self.options.append(SelectOption(i,i))


    def addOption(self, option:SelectOption):
        self.options.append(option)


class ComponentInteractionData:
    custom_id:str
    component_type:int
    values: [str]

    def __init__(self,d:dict):
        for k,v in d.items():
            self.__setattr__(k,v)
        if "values" in self.__dict__:
            tmp = []
            for i in self.values:
                tmp.append(i)
            self.values = tmp


class MemberData:
    id:int
    username:str
    nick:Union[str,None]

    def __init__(self,d):
        self.nick = d["nick"] if "nick" in d else None
        self.id = int(d["user"]["id"])
        self.username = d["user"]["username"]


class ComponentInteraction:
    raw: dict
    version: int
    type: int
    token: str
    message_id: int
    member_data: MemberData
    id: int
    channel_id: int
    guild_id: int
    data: ComponentInteractionData

    def __init__(self,d:dict):
        d = d["d"]
        for k,v in d.items():
            self.__setattr__(k,v)
        if "data" in self.__dict__:
            self.data = ComponentInteractionData(self.data)

        if "message" in self.__dict__:
            self.message_id = int(self.message["id"])
            self.__delattr__("message")

        if "member" in self.__dict__:
            self.member_data = MemberData(self.member)
            self.__delattr__("member")

        if "channel_id" in self.__dict__:
            self.channel_id = int(self.channel_id)

        if "guild_id" in self.__dict__:
            self.guild_id = int(self.guild_id)

        if "id" in self.__dict__:
            self.id = int(self.id)

        self.__delattr__("type")


class ActionRow(Component):
    components: [Component]

    def __init__(self, components=None, disabled: bool = False):
        super().__init__(1, disabled)

        if components is None:
            components = []
        self.components = components if components.__class__.__name__ == "list" else [components]


    def addComponent(self,component:Component):
        i = self.components.append(component)


class ComponentHelper:
    elements: [ActionRow]

    def __init__(self):
        self.elements = [ActionRow()]

    def addComponent(self, component:Component, line=0):
        self.elements[line].addComponent(component)

    def getComponents(self,id:str = None, **kwargs):
        tmp:[Component]
        tmp = []
        if id is not None:
            for i in self.elements:
                for a in i.components:
                    if a.custom_id == id:
                        tmp.append(a)

        for k,v in kwargs.items():
            for i in self.elements:
                for a in i.components:
                    if k in a.__dict__:
                        if a.__getattribute__(k) == v:
                            tmp.append(a)

        return tmp

    def getFirstComponent(self, id: str = None, **kwargs):
        if id is not None:
            for i in self.elements:
                for a in i.components:
                    if a.custom_id == id:
                        return a

        for k, v in kwargs.items():
            for i in self.elements:
                for a in i.components:
                    if k in a.__dict__:
                        if a.__getattribute__(k) == v:
                            return a


    @property
    def dict(self):
        return [todict(i) for i in self.elements]