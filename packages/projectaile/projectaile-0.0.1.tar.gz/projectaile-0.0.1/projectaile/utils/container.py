'''
    Class to store component initialization objects and entities
    that can be shared across pipelines and components
'''
class CONTAINER:
    initialized_components = dict()
    stored_entities = dict()
    
    @staticmethod
    def register_component(source_name, obj_instance):
        if CONTAINER.is_registered(source_name):
            raise RuntimeError(f'Component {source_name} already initialized')
            
        CONTAINER.initialized_components[source_name] = obj_instance

    @staticmethod
    def is_registered(source_name):
        return source_name in CONTAINER.initialized_components
    
    @staticmethod
    def is_stored(name):
        return name in CONTAINER.stored_entities
    
    @staticmethod
    def store_entity(name, entity):
        if CONTAINER.is_stored(name):
            raise RuntimeError(f'Entity {name} already stored.')
        
        CONTAINER.stored_entities[name] = entity
        
    @staticmethod
    def get_component(source_name):
        return CONTAINER.initialized_components[source_name]
    
    @staticmethod
    def get_entity(name):
        return CONTAINER.stored_entities[name]        