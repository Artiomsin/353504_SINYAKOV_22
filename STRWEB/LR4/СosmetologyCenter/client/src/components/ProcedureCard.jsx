import React from 'react';

const ProcedureCard = ({ name, price, durationMin }) => (
  <div 
    className="card procedure-card"
    onMouseEnter={() => console.log(`Навели на ${name}`)}
    onMouseLeave={() => console.log(`Убрали курсор с ${name}`)}
  >
    <h3>{name}</h3>
    <p>Цена: {price} ₽</p>
    <p>Длительность: {durationMin} мин</p>
  </div>
);

ProcedureCard.defaultProps = {
  name: 'Без названия',
  price: 0,
  durationMin: 0
};

export default ProcedureCard;
