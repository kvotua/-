import React, { useContext, useEffect } from "react";
import { useAppDispatch } from "src/app/hooks/useAppDispatch";
import { useAppSelector } from "src/app/hooks/useAppSelector";
import useGetTree from "src/app/hooks/useGetTree";
import {
  deleteNode,
  setCoreNewChild,
  setExistNewChild,
  setTree,
  setChildrens,
} from "src/app/store/slice/UserPgaeSlice";
import {
  useDeleteNodesMutation,
  usePostNodesMutation,
} from "src/app/store/slice/UserPgaeSlice/UserPageApi";
import { AddButton } from "src/shared/AddButton/AddButton";
import Back from "src/app/assets/icons/back.svg?react";
import Trash from "src/app/assets/icons/trash.svg?react";
import Exit from "src/app/assets/icons/exit.svg?react";
import { useNavigate, useParams } from "react-router-dom";
import { menuContext } from "src/app/context";
import { ITreeNode } from "src/app/types/nodes.types";
import { AnimatePresence, Reorder, motion } from "framer-motion";

const UserPage: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { projectId } = useParams();

  const nodes = useAppSelector((state) => state.userPage);
  const setNodes = (node_id: string, new_nodes: Array<string>) =>
    dispatch(setChildrens({ id: node_id, children: new_nodes }));
  const { tree, isTreeSuccess, templates } = useGetTree<ITreeNode>(projectId!);
  const { setMenuItems } = useContext(menuContext);
  const [deleteNodes] = useDeleteNodesMutation();

  const setBaseMenu = () => {
    const menuItem = [
      {
        handleClick: () => navigate(-1),
        Image: Exit,
      },
    ];
    setMenuItems(menuItem);
  };

  useEffect(() => {
    setBaseMenu();
    if (isTreeSuccess && tree) {
      dispatch(setTree(tree));
    }
  }, [isTreeSuccess, dispatch, tree, navigate, setMenuItems]);

  const [postNodes] = usePostNodesMutation();

  const addNode = async (id: string) => {
    const { data: newId } = (await postNodes({
      parent: id,
      template_id: templates![0],
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
    // console.log(id, clickedNodeId);

    return (
      <Reorder.Item value={id} key={id}>
        <motion.div
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
                  handleClick: () => setBaseMenu(),
                  Image: Back,
                },
                {
                  handleClick: () => {
                    handleDeleteNode(id);
                    setBaseMenu();
                  },
                  Image: Trash,
                },
              ]);
            }
          }}
          className="px-4 py-8 border-2 border-black w-full grid  text-4xl gap-4 rounded-20"
        >
          <Reorder.Group
            values={children.map((node) => node.id)}
            onReorder={(newOrder: Array<string>) => setNodes(id, newOrder)}
            className="h-full grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-4 "
          >
            {children?.map((child) => renderNode(child))}
          </Reorder.Group>
          <AddButton
            handleClick={() => {
              addNode(id);
            }}
          />
        </motion.div>
      </Reorder.Item>
    );
  };

  return (
    <div className="h-fit min-h-screen bg-white p-4">
      <AnimatePresence mode="popLayout" initial={false}>
        <Reorder.Group
          values={nodes.children.map((node) => node.id)}
          onReorder={(newOrder: Array<string>) => setNodes(nodes.id, newOrder)}
          className="h-full grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-4 "
        >
          {renderNode(nodes)}
        </Reorder.Group>
      </AnimatePresence>
      <AddButton
        handleClick={async () => {
          const { data: newId } = (await postNodes({
            parent: tree ? tree.id : "",
            template_id: templates![0],
          })) as { data: string };

          dispatch(setCoreNewChild({ id: newId, children: [] }));
        }}
      />
    </div>
  );
};

export default UserPage;
