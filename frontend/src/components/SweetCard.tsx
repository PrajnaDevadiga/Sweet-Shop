import React from 'react';
import { Sweet } from '../services/sweetsService';
import '../App.css';

interface SweetCardProps {
  sweet: Sweet;
  onPurchase: (id: number, quantity?: number) => void;
  onEdit?: (sweet: Sweet) => void;
  onDelete?: (id: number) => void;
  onRestock?: (id: number) => void;
}

const SweetCard: React.FC<SweetCardProps> = ({
  sweet,
  onPurchase,
  onEdit,
  onDelete,
  onRestock,
}) => {
  const isOutOfStock = sweet.quantity === 0;

  return (
    <div className="sweet-card">
      <h3>{sweet.name}</h3>
      <div className="category">📦 {sweet.category}</div>
      <div className="price">${sweet.price.toFixed(2)}</div>
      <div className={`quantity ${isOutOfStock ? 'out-of-stock' : ''}`}>
        {isOutOfStock ? '❌ Out of Stock' : `✅ In Stock: ${sweet.quantity}`}
      </div>

      <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '15px' }}>
        <button
          className="btn btn-primary"
          onClick={() => onPurchase(sweet.id, 1)}
          disabled={isOutOfStock}
          style={{ flex: 1, minWidth: '100px' }}
        >
          Purchase
        </button>

        {onEdit && (
          <button
            className="btn btn-secondary"
            onClick={() => onEdit(sweet)}
            style={{ flex: 1, minWidth: '80px' }}
          >
            Edit
          </button>
        )}

        {onDelete && (
          <button
            className="btn btn-danger"
            onClick={() => onDelete(sweet.id)}
            style={{ flex: 1, minWidth: '80px' }}
          >
            Delete
          </button>
        )}

        {onRestock && (
          <button
            className="btn btn-success"
            onClick={() => onRestock(sweet.id)}
            style={{ flex: 1, minWidth: '100px' }}
          >
            Restock
          </button>
        )}
      </div>
    </div>
  );
};

export default SweetCard;

