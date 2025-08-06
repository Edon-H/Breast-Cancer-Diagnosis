
<h2 class='sub-title'>🧬 Breast Cancer Diagnosis App </h2>

This interactive web application enables users to upload histopathology images and receive an instant prediction on whether the sample is **benign** or **malignant**, using a deep learning model trained on histopathology image data.
This interactive web application allows users to upload histopathology images and instantly receive a prediction indicating whether the sample is **benign** or **malign**. The prediction is powered by a deep learning model trained on real histopathology data.

---

@@ -35,18 +35,12 @@ Breast cancer is one of the most prevalent cancers in the world. Early detection

## 📊 Model Performance

- Model: VGG16 (Transfer Learning) with 3 convolutional layers
- Model: VGG16 (Transfer Learning) with custom classification head
- Image Size: 128 x 128
- Accuracy: **93.4%**
- Loss: 0.17

### 📈 Metrics Graphs

![Confusion Matrix](assets/team/bob.png)
*Confusion matrix showing true positives and negatives.*

![Training Curve](assets/team/bob.png)
*Model training and validation accuracy over epochs.*
- Training Data: 10,000 benign + 10,000 malignant images
- **Validation Accuracy:** **92.8%**
- **Validation Recall:** **92.8%**
- **Validation Loss:** **0.1938**

---
