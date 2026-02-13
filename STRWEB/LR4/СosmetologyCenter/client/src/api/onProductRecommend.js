export function onProductRecommend(analysis) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(
        "Рекомендуется регулярное очищение кожи, увлажнение и консультация специалиста."
      );
    }, 1000);
  });
}
