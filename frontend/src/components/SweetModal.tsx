import React, { useState, useEffect } from 'react';
import { Sweet, SweetCreate } from '../services/sweetsService';
import '../App.css';

interface SweetModalProps {
  sweet: Sweet | null;
  onClose: () => void;
  onSave: (sweet: SweetCreate) => void;
}

const SweetModal: React.FC<SweetModalProps> = ({ sweet, onClose, onSave }) => {
  const [formData, setFormData] = useState<SweetCreate>({
    name: '',
    category: '',
    price: 0,
    quantity: 0,
  });

  useEffect(() => {
    if (sweet) {
      setFormData({
        name: sweet.name,
        category: sweet.category,
        price: sweet.price,
        quantity: sweet.quantity,
      });
    } else {
      setFormData({
        name: '',
        category: '',
        price: 0,
        quantity: 0,
      });
    }
  }, [sweet]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.name && formData.category && formData.price > 0 && formData.quantity >= 0) {
      onSave(formData);
    }
  };

  const handleChange = (field: keyof SweetCreate, value: string | number) => {
    setFormData({
      ...formData,
      [field]: value,
    });
  };

  return (
    <div className="modal" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{sweet ? 'Edit Sweet' : 'Add New Sweet'}</h2>
          <button className="close-btn" onClick={onClose}>&times;</button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="name">Name *</label>
            <input
              type="text"
              id="name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="input-group">
            <label htmlFor="category">Category *</label>
            <input
              type="text"
              id="category"
              value={formData.category}
              onChange={(e) => handleChange('category', e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="price">Price *</label>
            <input
              type="number"
              id="price"
              value={formData.price}
              onChange={(e) => handleChange('price', parseFloat(e.target.value) || 0)}
              required
              min="0"
              step="0.01"
            />
          </div>

          <div className="input-group">
            <label htmlFor="quantity">Quantity *</label>
            <input
              type="number"
              id="quantity"
              value={formData.quantity}
              onChange={(e) => handleChange('quantity', parseInt(e.target.value) || 0)}
              required
              min="0"
            />
          </div>

          <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
            <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
              {sweet ? 'Update' : 'Create'}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              style={{ flex: 1 }}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SweetModal;

