# train_model.py
import os

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "static", "images", "training_images")
label_file = os.path.join(BASE_DIR, "training_labels.json")

import json
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split

class AccessDataset(Dataset):
    def __init__(self, image_dir, label_file, transform=None):
        self.image_dir = image_dir
        self.transform = transform
        with open(label_file, "r") as f:
            self.labels = json.load(f)
        self.image_files = list(self.labels.keys())

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        filename = self.image_files[idx]
        img_path = os.path.join(self.image_dir, filename)
        image = Image.open(img_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        label = self.labels[filename]
        target = torch.tensor([
            label["step_free_access"],
            label["clear_path"],
            label["readable_timetable"]
        ], dtype=torch.float32)

        return image, target

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    dataset = AccessDataset(image_dir, label_file, transform=transform)

    train_set, val_set = train_test_split(dataset, test_size=0.2, random_state=42)
    train_loader = DataLoader(train_set, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=16)

    model = models.resnet18(pretrained=True)
    model.fc = nn.Sequential(
        nn.Linear(model.fc.in_features, 3),
        nn.Sigmoid()  # für Multi-Label
    )
    model = model.to(device)

    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    EPOCHS = 10
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        for images, targets in train_loader:
            images, targets = images.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {running_loss/len(train_loader):.4f}")

    torch.save(model.state_dict(), "accessai_model.pth")
    print("✅ Modell gespeichert als accessai_model.pth")
