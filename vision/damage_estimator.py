# CV / simulated image-based damage scoring

import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np

from torchvision.models import resnet18, ResNet18_Weights

weights = ResNet18_Weights.DEFAULT
_model = resnet18(weights=weights)
_model.eval()

_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def estimate_damage_from_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        img_tensor = _transform(image).unsqueeze(0)

        with torch.no_grad():
            features = _model(img_tensor)

        severity = torch.sigmoid(features.mean()).item()
        return round(float(severity), 3)

    except Exception:
        # Fail-safe: moderate damage
        return 0.6
