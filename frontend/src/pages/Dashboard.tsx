import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { sweetsService, Sweet, SweetCreate } from '../services/sweetsService';
import SweetCard from '../components/SweetCard';
import SweetModal from '../components/SweetModal';
import SearchBar from '../components/SearchBar';
import '../App.css';

const Dashboard: React.FC = () => {
  const { logout, isAdmin } = useAuth();
  const [sweets, setSweets] = useState<Sweet[]>([]);
  const [filteredSweets, setFilteredSweets] = useState<Sweet[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingSweet, setEditingSweet] = useState<Sweet | null>(null);
  const [searchParams, setSearchParams] = useState({
    name: '',
    category: '',
    minPrice: '',
    maxPrice: '',
  });

  useEffect(() => {
    loadSweets();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [sweets, searchParams]);

  const loadSweets = async () => {
    try {
      setLoading(true);
      const data = await sweetsService.getAll();
      setSweets(data);
      setFilteredSweets(data);
    } catch (err: any) {
      setError('Failed to load sweets. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = async () => {
    try {
      const params: any = {};
      if (searchParams.name) params.name = searchParams.name;
      if (searchParams.category) params.category = searchParams.category;
      if (searchParams.minPrice) params.min_price = parseFloat(searchParams.minPrice);
      if (searchParams.maxPrice) params.max_price = parseFloat(searchParams.maxPrice);

      if (Object.keys(params).length > 0) {
        const results = await sweetsService.search(params);
        setFilteredSweets(results);
      } else {
        setFilteredSweets(sweets);
      }
    } catch (err) {
      console.error('Search failed:', err);
      setFilteredSweets(sweets);
    }
  };

  const handlePurchase = async (id: number, quantity: number = 1) => {
    try {
      await sweetsService.purchase(id, quantity);
      await loadSweets();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Purchase failed. Please try again.');
    }
  };

  const handleAddSweet = () => {
    setEditingSweet(null);
    setShowModal(true);
  };

  const handleEditSweet = (sweet: Sweet) => {
    setEditingSweet(sweet);
    setShowModal(true);
  };

  const handleSaveSweet = async (sweetData: SweetCreate) => {
    try {
      if (editingSweet) {
        await sweetsService.update(editingSweet.id, sweetData);
      } else {
        await sweetsService.create(sweetData);
      }
      setShowModal(false);
      setEditingSweet(null);
      await loadSweets();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to save sweet. Please try again.');
    }
  };

  const handleDeleteSweet = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this sweet?')) {
      return;
    }

    try {
      await sweetsService.delete(id);
      await loadSweets();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete sweet. Please try again.');
    }
  };

  const handleRestock = async (id: number) => {
    const quantity = prompt('Enter restock quantity:');
    if (!quantity || isNaN(parseInt(quantity)) || parseInt(quantity) <= 0) {
      return;
    }

    try {
      await sweetsService.restock(id, parseInt(quantity));
      await loadSweets();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Restock failed. Please try again.');
    }
  };

  return (
    <div>
      <div className="navbar">
        <h1>🍬 Sweet Shop Management</h1>
        <div className="navbar-actions">
          <span className="user-info">
            {isAdmin() ? '👑 Admin' : '👤 User'}
          </span>
          <button className="btn btn-secondary" onClick={logout}>
            Logout
          </button>
        </div>
      </div>

      <div className="container">
        {error && (
          <div style={{
            padding: '12px',
            background: '#fee',
            color: '#c33',
            borderRadius: '6px',
            marginBottom: '20px'
          }}>
            {error}
          </div>
        )}

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2 style={{ margin: 0, color: '#333' }}>Available Sweets</h2>
            {isAdmin() && (
              <button className="btn btn-primary" onClick={handleAddSweet}>
                + Add New Sweet
              </button>
            )}
          </div>

          <SearchBar
            searchParams={searchParams}
            onSearchChange={setSearchParams}
          />

          {loading ? (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <p>Loading sweets...</p>
            </div>
          ) : filteredSweets.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <p>No sweets found. {isAdmin() && 'Add some sweets to get started!'}</p>
            </div>
          ) : (
            <div className="grid">
              {filteredSweets.map((sweet) => (
                <SweetCard
                  key={sweet.id}
                  sweet={sweet}
                  onPurchase={handlePurchase}
                  onEdit={isAdmin() ? handleEditSweet : undefined}
                  onDelete={isAdmin() ? handleDeleteSweet : undefined}
                  onRestock={isAdmin() ? handleRestock : undefined}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {showModal && (
        <SweetModal
          sweet={editingSweet}
          onClose={() => {
            setShowModal(false);
            setEditingSweet(null);
          }}
          onSave={handleSaveSweet}
        />
      )}
    </div>
  );
};

export default Dashboard;

