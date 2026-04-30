import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interactions",
  initialState: {
    data: [],
    search: "",
    sentimentFilter: "all"
  },
  reducers: {
    setData: (state, action) => {
      state.data = action.payload;
    },
    setSearch: (state, action) => {
      state.search = action.payload;
    },
    setSentimentFilter: (state, action) => {
      state.sentimentFilter = action.payload;
    }
  }
});

export const { setData, setSearch, setSentimentFilter } =
  interactionSlice.actions;

export default interactionSlice.reducer;