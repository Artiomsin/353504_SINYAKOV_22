import React, { useState, useMemo } from "react";
import "../styles/SkinAnalyzer.css";

export default function SkinAnalyzer() {
  const [photo, setPhoto] = useState(null);
  const [photoPreview, setPhotoPreview] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [recommendations, setRecommendations] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingRec, setLoadingRec] = useState(false);

  const handlePhotoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPhoto(file);
      const reader = new FileReader();
      reader.onloadend = () => setPhotoPreview(reader.result);
      reader.readAsDataURL(file);
    }
  };

  // ================== XMLHttpRequest для анализа кожи ==================
  const analyzeSkin = () => {
    if (!photo) {
      alert("Загрузите фото!");
      return Promise.reject("Нет фото");
    }

    setLoading(true);
    setAnalysis(null);
    setRecommendations("");

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      formData.append("photo", photo);

      xhr.open("POST", "http://localhost:4000/api/skin/analyze", true);
      xhr.withCredentials = true; // Для отправки cookies

      xhr.onload = function() {
        setLoading(false);
        
        if (xhr.status === 200) {
          try {
            const data = JSON.parse(xhr.responseText);
            setAnalysis(data);
            resolve(data);
          } catch (err) {
            console.error("Ошибка парсинга JSON:", err);
            alert("Ошибка обработки ответа от сервера");
            reject(err);
          }
        } else {
          console.error(`HTTP ошибка: ${xhr.status}`, xhr.statusText);
          alert(`Ошибка анализа кожи: ${xhr.status} ${xhr.statusText}`);
          reject(new Error(`HTTP ${xhr.status}`));
        }
      };

      xhr.onerror = function() {
        setLoading(false);
        console.error("Ошибка сети XMLHttpRequest");
        alert("Ошибка сети при анализе кожи");
        reject(new Error("Network error"));
      };

      xhr.ontimeout = function() {
        setLoading(false);
        console.error("Таймаут XMLHttpRequest");
        alert("Таймаут при анализе кожи");
        reject(new Error("Request timeout"));
      };

      // Устанавливаем таймаут 30 секунд
      xhr.timeout = 30000;
      
      // Отправляем запрос
      xhr.send(formData);
    });
  };

  // ================== XMLHttpRequest для рекомендаций ==================
  const getRecommendations = () => {
    if (!analysis) {
      alert("Сначала сделайте анализ!");
      return Promise.reject("Нет данных анализа");
    }

    setLoadingRec(true);

    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      
      xhr.open("POST", "http://localhost:4000/api/skin/recommend", true);
      xhr.withCredentials = true;
      xhr.setRequestHeader("Content-Type", "application/json");

      xhr.onload = function() {
        setLoadingRec(false);
        
        if (xhr.status === 200) {
          try {
            const data = JSON.parse(xhr.responseText);
            setRecommendations(data.recommendations);
            resolve(data);
          } catch (err) {
            console.error("Ошибка парсинга JSON рекомендаций:", err);
            alert("Ошибка обработки рекомендаций");
            reject(err);
          }
        } else {
          console.error(`HTTP ошибка рекомендаций: ${xhr.status}`);
          alert(`Ошибка получения рекомендаций: ${xhr.status}`);
          reject(new Error(`HTTP ${xhr.status}`));
        }
      };

      xhr.onerror = function() {
        setLoadingRec(false);
        console.error("Ошибка сети при получении рекомендаций");
        alert("Ошибка сети при получении рекомендаций");
        reject(new Error("Network error"));
      };

      xhr.ontimeout = function() {
        setLoadingRec(false);
        console.error("Таймаут получения рекомендаций");
        alert("Таймаут при получении рекомендаций");
        reject(new Error("Recommendation timeout"));
      };

      xhr.timeout = 30000;
      
      // Отправляем данные анализа
      xhr.send(JSON.stringify({ skinAnalysis: analysis }));
    });
  };

  // ================== Обработчик клика (для совместимости) ==================
  const handleAnalyzeClick = () => {
    analyzeSkin().catch(err => {
      console.error("Ошибка в handleAnalyzeClick:", err);
    });
  };

  const handleGetRecommendationsClick = () => {
    getRecommendations().catch(err => {
      console.error("Ошибка в handleGetRecommendationsClick:", err);
    });
  };

  const getPercentageColor = (percent) => {
    const num = parseFloat(percent);
    if (num > 70) return "var(--danger)";
    if (num > 40) return "var(--warning)";
    return "var(--success)";
  };

  const formatRecommendations = (text) => {
    if (!text) return [];
    const paragraphs = text.split("\n\n").filter((p) => p.trim());
    return paragraphs;
  };

  const formatRecommendationLine = (line, isBold = false) => {
    const cleanLine = line.replace(/^\d+\.\s/, "").replace(/^[-•]\s/, "").trim();
    if (isBold || line.includes("**") || line.match(/^[А-Я].*:/)) {
      return <strong>{cleanLine.replace(/\*\*/g, "")}</strong>;
    }
    return cleanLine.split(/\*\*/).map((part, index) =>
      index % 2 === 1 ? <strong key={index}>{part}</strong> : part
    );
  };

  const getParagraphType = (paragraph) => {
    const firstLine = paragraph.split("\n")[0];
    if (firstLine.includes("Судя по") || firstLine.includes("**")) return "intro";
    if (firstLine.includes("Рекомендации")) return "title";
    if (paragraph.includes("1.") || paragraph.includes("2.") || paragraph.includes("3.")) return "list";
    return "regular";
  };

  // ---------------------------
  // useMemo для анализа кожи
  // ---------------------------
  const formattedAnalysis = useMemo(() => {
    if (!analysis) return [];
    if (analysis.analysis?.formatted) {
      return analysis.analysis.formatted.map((item) => ({
        ...item,
        displayPercentage: item.percentage || (item.value * 100).toFixed(1),
        color:
          item.value > 0.7 ? "var(--danger)" :
          item.value > 0.4 ? "var(--warning)" :
          "var(--success)",
      }));
    }
    if (analysis.formatted) {
      return analysis.formatted
        .split("\n")
        .map((line) => {
          const match = line.match(/(.+?) — (\d+\.?\d*)%/);
          if (!match) return null;
          const [, name, percent] = match;
          return { name: name.trim(), displayPercentage: percent, color: getPercentageColor(percent) };
        })
        .filter(Boolean);
    }
    return [];
  }, [analysis]);

  return (
    <div className="skin-analyzer">
      <div className="container">
        <h2 className="title">🧬 Анализ кожи</h2>

        {/* Загрузка фото */}
        <div className="upload-section">
          <div className="file-input-container">
            <label className="file-input-label">
              <input
                type="file"
                accept="image/*"
                onChange={handlePhotoChange}
                className="file-input"
              />
              <span className="upload-button">📸 Выбрать фото</span>
            </label>
            {photo && <span className="file-name">{photo.name}</span>}
          </div>

          {photoPreview && (
            <div className="photo-preview">
              <img src={photoPreview} alt="Предпросмотр" />
            </div>
          )}

          <button
            onClick={handleAnalyzeClick}
            disabled={loading || !photo}
            className="analyze-button"
          >
            {loading ? (
              <>
                <span className="spinner"></span> Анализируем...
              </>
            ) : (
              "🔍 Анализировать кожу"
            )}
          </button>
        </div>

        {/* Результаты анализа */}
        {formattedAnalysis.length > 0 && (
          <div className="results-section">
            <h3 className="section-title">
              📊 Результат анализа
              {analysis.summary && (
                <span className="confidence-badge">
                  Достоверность: {analysis.summary.confidence}%
                </span>
              )}
            </h3>

            <div className="analysis-grid">
              {formattedAnalysis.map((item, index) => (
                <div key={index} className="analysis-item">
                  <div className="analysis-header">
                    <span className="item-index">#{index + 1}</span>
                    <span className="item-name">{item.name}</span>
                  </div>
                  <div className="progress-container">
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{
                          width: `${item.displayPercentage}%`,
                          backgroundColor: item.color,
                        }}
                      ></div>
                    </div>
                    <span
                      className="percentage"
                      style={{ color: item.color }}
                    >
                      {item.displayPercentage}%
                    </span>
                  </div>
                  <div className="item-level">
                    {item.level ||
                      (item.value > 0.7
                        ? "🔴 Высокая вероятность"
                        : item.value > 0.4
                        ? "🟡 Средняя вероятность"
                        : "🟢 Низкая вероятность")}
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleGetRecommendationsClick}
              disabled={loadingRec}
              className="recommend-button"
            >
              {loadingRec ? (
                <>
                  <span className="spinner"></span> Генерируем рекомендации...
                </>
              ) : (
                "💡 Получить рекомендации по уходу"
              )}
            </button>
          </div>
        )}

        {/* Рекомендации */}
        {recommendations && (
          <div className="recommendations-section">
            <h3 className="section-title">🌟 Рекомендации по уходу</h3>
            <div className="recommendations-card">
              <div className="recommendations-content">
                {formatRecommendations(recommendations).map((paragraph, paraIndex) => {
                  const type = getParagraphType(paragraph);
                  const lines = paragraph.split("\n").filter(line => line.trim());
                  return (
                    <div key={paraIndex} className={`recommendation-paragraph ${type}`}>
                      {lines.map((line, lineIndex) => {
                        const isListItem = line.match(/^\d+\./);
                        const isBold = type === "title" || type === "intro" || line.includes("**");
                        return (
                          <div key={lineIndex} className={`rec-line ${isListItem ? 'list-item' : ''}`}>
                            {isListItem && (
                              <div className="list-marker">
                                <span className="list-number">{line.match(/^\d+/)[0]}</span>
                              </div>
                            )}
                            <div className="rec-text">{formatRecommendationLine(line, isBold)}</div>
                          </div>
                        );
                      })}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}