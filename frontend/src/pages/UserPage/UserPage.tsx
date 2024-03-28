import React, { useContext, useEffect } from "react";
import { useAppDispatch } from "src/app/hooks/useAppDispatch";
import { useAppSelector } from "src/app/hooks/useAppSelector";
import useGetTree from "src/app/hooks/useGetTree";
import {
  deleteNode,
  setCoreNewChild,
  setExistNewChild,
  setTree,
} from "src/app/store/slice/UserPgaeSlice";
import {
  useDeleteNodesMutation,
  usePostNodesMutation,
} from "src/app/store/slice/UserPgaeSlice/UserPageApi";
import { AddButton } from "src/shared/AddButton/AddButton";
import Back from "src/app/assets/icons/back.svg?react";
import Trash from "src/app/assets/icons/trash.svg?react";
import { useNavigate } from "react-router-dom";
import { menuContext } from "src/app/context";
import { ITreeNode } from "src/app/types/nodes.types";
import { AnimatePresence, motion } from "framer-motion";

const UserPage: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const nodes = useAppSelector((state) => state.userPage);
  const { tree, isTreeSuccess } = useGetTree<ITreeNode>();
  const { setMenuItems } = useContext(menuContext);
  const [deleteNodes] = useDeleteNodesMutation();

  useEffect(() => {
    const menuItem = [
      {
        handleClick: () => navigate(-1),
        Image: Back,
      },
    ];
    setMenuItems(menuItem);
    if (isTreeSuccess && tree) {
      dispatch(setTree(tree));
    }
  }, [isTreeSuccess, dispatch, tree, navigate, setMenuItems]);

  const [postNodes] = usePostNodesMutation();

  const addNode = async (id: string) => {
    const { data: newId } = (await postNodes({
      parent: id,
      children: [],
    })) as { data: string };
    const newChild: ITreeNode = {
      id: newId,
      children: [],
    };
    dispatch(setExistNewChild({ newChild: newChild, id: id }));
  };

  const handleDeleteNode = (id: string) => {
    deleteNodes(id);
    dispatch(deleteNode(id));
  };

  const renderNode = ({ id, children }: ITreeNode): React.ReactNode => {
    if (isTreeSuccess && tree && id === tree.id) {
      return children?.map((child) => renderNode(child));
    }
    return (
      <motion.div
        key={id}
        initial={{
          scale: 0,
        }}
        animate={{
          scale: 1,
        }}
        exit={{
          scale: 0,
        }}
        transition={{
          duration: 0.3,
        }}
        onClick={(event) => {
          if (event.target === event.currentTarget) {
            setMenuItems([
              {
                handleClick: () => navigate(-1),
                Image: Back,
              },
              {
                handleClick: () => {
                  handleDeleteNode(id);
                  setMenuItems([
                    {
                      handleClick: () => navigate(-1),
                      Image: Back,
                    },
                  ]);
                },
                Image: Trash,
              },
            ]);
          }
        }}
        className="px-4 py-8 border-2 border-black w-full grid  text-4xl gap-4 rounded-20"
      >
        {children?.map((child) => renderNode(child))}
        <AddButton
          handleClick={() => {
            addNode(id);
          }}
        />
      </motion.div>
    );
  };

  return (
    <div className="h-full min-h-screen bg-white grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-4 p-4">
      <AnimatePresence mode="popLayout" initial={false}>
        {renderNode(nodes)}
      </AnimatePresence>
      <AddButton
        handleClick={async () => {
          const { data: newId } = (await postNodes({
            parent: tree ? tree.id : "",
            children: [],
          })) as { data: string };

          dispatch(setCoreNewChild({ id: newId, children: [] }));
        }}
      />
    </div>
  );
};

export { UserPage };
