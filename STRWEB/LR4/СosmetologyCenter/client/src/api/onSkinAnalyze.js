export function onSkinAnalyze(photo) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("photo", photo);

    xhr.open("POST", "http://localhost:4000/api/skin/analyze");

    xhr.onload = () => {
      xhr.status === 200
        ? resolve(JSON.parse(xhr.responseText))
        : reject();
    };

    xhr.onerror = reject;
    xhr.send(formData);
  });
}
