# ai_model.py

import torch
from torchvision import models, transforms
from PIL import Image

# Modellstruktur wie im Training
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18(weights=None)
model.fc = torch.nn.Sequential(
    torch.nn.Linear(model.fc.in_features, 3),
    torch.nn.Sigmoid()
)
model.load_state_dict(torch.load("accessai_model.pth", map_location=device))
model.to(device)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_accessibility(image_path):
    img = Image.open(image_path).convert("RGB")
    input_tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)[0].cpu().numpy()

    prediction = {
        "lift_working": int(output[0] > 0.5),
        "path_clear": int(output[1] > 0.5),
        "readable_info": int(output[2] > 0.5),
        "confidence": {
            "lift_working": round(float(output[0]), 2),
            "path_clear": round(float(output[1]), 2),
            "readable_info": round(float(output[2]), 2),
        }
    }

    return prediction
