{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a603c03c",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "model = build_model()\n",
    "history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32)\n",
    "model.save('model.keras')"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
