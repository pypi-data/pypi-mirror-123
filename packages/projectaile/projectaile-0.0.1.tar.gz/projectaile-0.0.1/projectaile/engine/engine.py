from projectaile.utils import BASE
from projectaile.config import CONFIG
from projectaile.pipelines import PIPELINE

class ENGINE(BASE):
    def __init__(self, config: CONFIG, model_pipeline: PIPELINE, data_pipeline: PIPELINE):
        self._config = config
        self.data_pipeline = data_pipeline
        self.model_pipeline = model_pipeline
        
        self.initialize(config)
        
    def run(self):
        pass
    
    def save(self):
        self.saver.save(self.data_pipeline.dump_state())
        self.saver.save(self.model_pipeline.dump_state())