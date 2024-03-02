import React, { useState } from "react";
import { useAppDispatch } from "src/app/hooks/useAppDispatch";
import { useAppSelector } from "src/app/hooks/useAppSelector";
import { setPage } from "src/app/store/slice/UserPgaeSlice";
import { AddButton } from "src/shared/AddButton/AddButton";

interface IInitialState {
  id: string;
  children?: IInitialState[] | null;
}

const UserPage: React.FC = () => {
  const dispatch = useAppDispatch();
  const nodes = useAppSelector((state) => state.userPage);

  const [id, setId] = useState<number>(0);

  const addNode = (id: string, children: IInitialState[] | null) => {
    dispatch(setPage({ id, children }));
  };

  const renderNode = ({ id, children }: IInitialState) => {
    return (
      <div
        key={id}
        className="px-4 py-8 border-2 border-black w-full grid  text-4xl gap-4 rounded-20"
      >
        {children?.map((child) => renderNode(child))}
        <AddButton
          handleClick={() => {
            addNode(id, children!);
          }}
        />
      </div>
    );
  };
  return (
    <div className="h-full min-h-screen bg-white grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-4 p-4">
      {nodes.map((node) => renderNode(node))}
      <AddButton
        handleClick={() => {
          setId((prev) => prev + 1);
          addNode(id.toString(), null);
        }}
      />
    </div>
  );
};

export { UserPage };
