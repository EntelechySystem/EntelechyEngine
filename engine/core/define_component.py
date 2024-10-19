"""
定义组件

#HACK 没有做覆盖性的单元测试。目前只要求能够在主程序中正确运行就好。
"""
from engine.externals import Union, Any


class AttributeComponent:
    """
    特征组件。

    用于描述一个事物的特征。

    具有的特征有：

    - id (Union[str, None]): 事物之编号
    - entity_name (Union[str, None]): 事物之名称
    - text_name (Union[str, None]): 事物之文本名称
    - entity_type (Union[str, None]): 事物之实体类型
    - structure_type (Union[str, None]): 事物之结构类型
    - container_type (Union[str, None]): 事物之容器类型
    - process_type (Union[str, None]): 事物之过程类型
    - content_type (Union[str, None]): 事物之内容类型
    - content_name (Union[str, None]): 事物之内容名称
    - other (Union[dict, Any]): 事物之其他特征

    """

    id: Union[str, None]  # 事物之编号
    entity_name: Union[str, None]  # 事物之名称
    text_name: Union[str, None]  # 事物之文本名称
    entity_type: Union[str, None]  # 事物之实体类型
    structure_type: Union[str, None]  # 事物之结构类型
    container_type: Union[str, None]  # 事物之容器类型
    process_type: Union[str, None]  # 事物之过程类型
    content_type: Union[str, None]  # 事物之内容类型
    content_name: Union[str, None]  # 事物之内容名称
    other: Union[dict, Any]  # 事物之其他特征

    def __init__(self, attribute: AttributeComponentType = None, **kwargs):
        """
        初始化特征组件。

        Args:
            attribute: 特征数据
            kwargs (): 其它参数

        > [!note]
        > 以下是赋值的要求：

        - 如果`attribute`不为空，那么要求`**kwargs`设置为空；

        - 如果`attribute`为空且`**kwargs`不为空，那么要求`**kwargs`里面不能有`attribute`；

        """

        ## 如果`attribute`不为空，那么直接设置`attribute`之内容，否则设置`**kwargs`之内容
        if attribute is not None:
            kwargs = None
            if attribute['id'] is not None:
                self.id = str(attribute['id']).zfill(8)
            else:
                raise ValueError("id不能为空")  # 如果id为空，则报错
                pass  # if
            if attribute['entity_name'] is not None:
                self.entity_name = attribute['entity_name']
            else:
                raise ValueError("entity_name不能为空")  # 如果entity_name为空，则报错
                pass  # if
            self.text_name = attribute['text_name'] if 'text_name' in attribute.keys() else None
            self.entity_type = attribute['entity_type'] if 'entity_type' in attribute.keys() else None
            self.structure_type = attribute['structure_type'] if 'structure_type' in attribute.keys() else None
            self.container_type = attribute['container_type'] if 'container_type' in attribute.keys() else None
            self.process_type = attribute['process_type'] if 'process_type' in attribute.keys() else None
            self.content_type = attribute['content_type'] if 'content_type' in attribute.keys() else None
            self.content_name = attribute['content_name'] if 'content_name' in attribute.keys() else None
            ## 创建其他特征字典
            self.other = dict()
            for k, v in attribute.items():
                if not (k == "id" or k == "entity_name" or k == "text_name" or k == "entity_type" or k == "structure_type" or k == "container_type" or k == "process_type" or k == "content_type" or k == "content_name"):
                    for kk, vv in v.items():
                        self.other.update({kk: vv})
                        pass  # for
                    # self.other.update({k: v})
                    pass  # if
                pass  # for
        else:
            if kwargs['id'] is not None:
                self.id = kwargs['id']
            else:
                raise ValueError("id不能为空")  # 如果id为空，则报错
                pass  # if
            if kwargs['entity_name'] is not None:
                self.entity_name = kwargs['entity_name']
            else:
                raise ValueError("entity_name不能为空")  # 如果entity_name为空，则报错
                pass  # if
            self.text_name = kwargs['text_name'] if 'text_name' in kwargs.keys() else None
            self.entity_type = kwargs['entity_type'] if 'entity_type' in kwargs.keys() else None
            self.structure_type = kwargs['structure_type'] if 'structure_type' in kwargs.keys() else None
            self.container_type = kwargs['container_type'] if 'container_type' in kwargs.keys() else None
            self.process_type = kwargs['process_type'] if 'process_type' in kwargs.keys() else None
            self.content_type = kwargs['content_type'] if 'content_type' in kwargs.keys() else None
            self.content_name = kwargs['content_name'] if 'content_name' in kwargs.keys() else None
            ## 创建其他特征字典
            self.other = dict()
            for k, v in kwargs.items():
                if not (k == "id" or k == "entity_name" or k == "text_name" or k == "entity_type" or k == "structure_type" or k == "container_type" or k == "process_type" or k == "content_type" or k == "content_name"):
                    self.other.update({k: v})
                    pass  # if
                pass  # for
            pass  # if

        pass  # function

    pass  # class


class ContentComponent:
    """
    内容组件
    """

    content: NodeComponentType

    def __init__(self, content):
        """

        Args:
            content: 内容
        """
        self.content = content if content is not None else None

    pass  # class


class ContainerComponent:
    """
    容器组件
    """

    container: ContainerComponentType

    def __init__(self, container):
        """

        Args:
            container: 容器之内容
        """
        self.container = container if container is not None else None
        pass  # function

    pass  # class


class ProcessComponent:
    """
    过程组件
    """

    process: ProcessComponentType

    def __init__(self, process):
        """

        Args:
            process: 过程之内容
        """
        self.process = process if process is not None else None
        pass  # function

    pass  # class


class ExecuteComponent:
    """
    执行组件
    """

    execute: ExecuteComponentType

    def __init__(self, execute):
        """

        Args:
            execute: 执行之内容
        """
        self.execute = execute if execute is not None else None
        pass  # function

    pass  # class


class OperateComponent:
    """
    运作组件
    """

    operate: OperateComponentType

    def __init__(self, operate):
        """

        Args:
            operate: 运作之内容
        """
        self.operate = operate if operate is not None else None
        pass  # function

    pass  # class


class EnvironmentComponent:
    """
    环境组件
    """

    environment: EnvironmentComponentType

    def __init__(self, environment):
        """

        Args:
            environment: 环境之内容
        """
        self.environment = environment if environment is not None else None
        pass  # function

    pass  # class


class AlgorithmComponent:
    """
    算法组件
    """

    algorithm: AlgorithmComponentType

    def __init__(self, algorithm):
        """

        Args:
            algorithm: 环境之内容
        """
        self.algorithm = algorithm if algorithm is not None else None
        pass  # function

    pass  # class


class NodeComponent:
    """
    节点组件
    """

    node: NodeComponentType

    def __init__(self, node):
        """

        Args:
            node: 节点之内容
        """
        self.node = node if node is not None else None
        pass  # function

    pass  # class


class ConditionComponent:
    """
    条件组件
    """

    condition: ConditionComponentType

    def __init__(self, condition):
        """

        Args:
            condition: 条件之内容
        """
        self.condition = condition if condition is not None else None
        pass  # function

    pass  # class
