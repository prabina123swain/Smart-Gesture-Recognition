import os
import sys
import yaml
import shutil
from signLanguage.utils.main_utils import read_yaml_file
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifacts_entity import ModelTrainerArtifact

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")

            # Use Windows-friendly command
            shutil.unpack_archive("Sign_language_data.zip", ".")

            # Delete ZIP file
            os.remove("Sign_language_data.zip")

            # Ensure data.yaml exists
            if not os.path.exists("data.yaml"):
                raise FileNotFoundError("data.yaml not found after extraction!")

            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            print(model_config_file_name)

            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = int(num_classes)

            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            os.system(f"cd yolov5 && python train.py --img 416 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_epochs} --data ../data.yaml --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results --cache")

            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            shutil.copy("yolov5/runs/train/yolov5s_results/weights/best.pt", self.model_trainer_config.model_trainer_dir)

            # Cleanup
            shutil.rmtree("yolov5/runs", ignore_errors=True)
            shutil.rmtree("train", ignore_errors=True)
            shutil.rmtree("test", ignore_errors=True)
            if os.path.exists("data.yaml"):
                os.remove("data.yaml")

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path="yolov5/best.pt")

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise SignException(e, sys)
