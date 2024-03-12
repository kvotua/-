import React, { useEffect } from "react";
import { useAppDispatch } from "src/app/hooks/useAppDispatch";
import { useAppSelector } from "src/app/hooks/useAppSelector";
import useGetTree from "src/app/hooks/useGetTree";
import {
  setCoreNewChild,
  setExistNewChild,
  setTree,
} from "src/app/store/slice/UserPgaeSlice";
import { usePostNodesMutation } from "src/app/store/slice/UserPgaeSlice/UserPageApi";
import { AddButton } from "src/shared/AddButton/AddButton";

export interface IInitialState {
  id: string;
  children: IInitialState[];
}

const UserPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const nodes = useAppSelector((state) => state.userPage);
  const { tree, isTreeSuccess } = useGetTree();

  useEffect(() => {
    if (isTreeSuccess) {
      dispatch(setTree(tree));
    }
  }, [isTreeSuccess, dispatch, tree]);

  const [postNodes] = usePostNodesMutation();

  const addNode = async (id: string) => {
    const { data: newId } = (await postNodes({
      parent: id,
      children: [],
    })) as { data: string };
    const newChild: IInitialState = {
      id: newId,
      children: [],
    };
    dispatch(setExistNewChild({ newChild: newChild, id: id }));
  };

  const renderNode = ({ id, children }: IInitialState): React.ReactNode => {
    if (isTreeSuccess && id === tree.id) {
      return children?.map((child) => renderNode(child));
    }
    return (
      <div
        key={id}
        className="px-4 py-8 border-2 border-black w-full grid  text-4xl gap-4 rounded-20"
      >
        {children?.map((child) => renderNode(child))}
        <AddButton
          handleClick={() => {
            addNode(id);
          }}
        />
      </div>
    );
  };

  return (
    <div className="h-full min-h-screen bg-white grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-4 p-4">
      {renderNode(nodes)}
      <AddButton
        handleClick={async () => {
          const { data: newId } = (await postNodes({
            parent: tree.id,
            children: [],
          })) as { data: string };

          dispatch(setCoreNewChild({ id: newId, children: [] }));
        }}
      />
    </div>
  );
};

export { UserPage };
