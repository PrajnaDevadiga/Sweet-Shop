import React from 'react';
import '../App.css';

interface SearchParams {
  name: string;
  category: string;
  minPrice: string;
  maxPrice: string;
}

interface SearchBarProps {
  searchParams: SearchParams;
  onSearchChange: (params: SearchParams) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ searchParams, onSearchChange }) => {
  const handleChange = (field: keyof SearchParams, value: string) => {
    onSearchChange({
      ...searchParams,
      [field]: value,
    });
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search by name..."
        value={searchParams.name}
        onChange={(e) => handleChange('name', e.target.value)}
      />
      <input
        type="text"
        placeholder="Category..."
        value={searchParams.category}
        onChange={(e) => handleChange('category', e.target.value)}
      />
      <input
        type="number"
        placeholder="Min price"
        value={searchParams.minPrice}
        onChange={(e) => handleChange('minPrice', e.target.value)}
        min="0"
        step="0.01"
      />
      <input
        type="number"
        placeholder="Max price"
        value={searchParams.maxPrice}
        onChange={(e) => handleChange('maxPrice', e.target.value)}
        min="0"
        step="0.01"
      />
      {(searchParams.name || searchParams.category || searchParams.minPrice || searchParams.maxPrice) && (
        <button
          className="btn btn-secondary"
          onClick={() => onSearchChange({ name: '', category: '', minPrice: '', maxPrice: '' })}
        >
          Clear
        </button>
      )}
    </div>
  );
};

export default SearchBar;

