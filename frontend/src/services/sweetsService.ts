import api from './api';

export interface Sweet {
  id: number;
  name: string;
  category: string;
  price: number;
  quantity: number;
}

export interface SweetCreate {
  name: string;
  category: string;
  price: number;
  quantity: number;
}

export interface SearchParams {
  name?: string;
  category?: string;
  min_price?: number;
  max_price?: number;
}

export const sweetsService = {
  getAll: async (): Promise<Sweet[]> => {
    const response = await api.get('/sweets');
    return response.data;
  },

  search: async (params: SearchParams): Promise<Sweet[]> => {
    const queryParams = new URLSearchParams();
    if (params.name) queryParams.append('name', params.name);
    if (params.category) queryParams.append('category', params.category);
    if (params.min_price !== undefined) queryParams.append('min_price', params.min_price.toString());
    if (params.max_price !== undefined) queryParams.append('max_price', params.max_price.toString());
    
    const response = await api.get(`/sweets/search?${queryParams.toString()}`);
    return response.data;
  },

  getById: async (id: number): Promise<Sweet> => {
    const response = await api.get(`/sweets/${id}`);
    return response.data;
  },

  create: async (sweet: SweetCreate): Promise<Sweet> => {
    const response = await api.post('/sweets', sweet);
    return response.data;
  },

  update: async (id: number, sweet: Partial<SweetCreate>): Promise<Sweet> => {
    const response = await api.put(`/sweets/${id}`, sweet);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/sweets/${id}`);
  },

  purchase: async (id: number, quantity: number = 1): Promise<Sweet> => {
    const response = await api.post(`/sweets/${id}/purchase`, { quantity });
    return response.data;
  },

  restock: async (id: number, quantity: number): Promise<Sweet> => {
    const response = await api.post(`/sweets/${id}/restock`, { quantity });
    return response.data;
  },
};

