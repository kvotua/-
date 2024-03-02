import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface IInitialState {
  id: string;
  children?: IInitialState[] | null;
}

const initialState: IInitialState[] = [];

export const userPageSlice = createSlice({
  name: "projects",
  initialState,
  reducers: {
    setPage(state, action: PayloadAction<IInitialState>) {
      const { id } = action.payload;
      const existingItem = findIdInNestedObjects(state, id);

      if (!existingItem) {
        state.push(action.payload);
      } else {
        const newChild: IInitialState = {
          id: `${id}_${(existingItem.children?.length || 0) + 1}`,
          children: [],
        };
        existingItem.children = existingItem.children
          ? [...existingItem.children, newChild]
          : [newChild];
      }
    },
  },
});

const findIdInNestedObjects = (
  obj: IInitialState[],
  targetId: string,
): IInitialState | null => {
  for (const item of obj) {
    if (item.id === targetId) {
      return item;
    }
    if (item.children && item.children.length > 0) {
      const result = findIdInNestedObjects(item.children, targetId);
      if (result) {
        return result;
      }
    }
  }
  return null;
};

export const { setPage } = userPageSlice.actions;
export default userPageSlice.reducer;
