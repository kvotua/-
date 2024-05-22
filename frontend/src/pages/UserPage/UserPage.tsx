import React, { useContext, useEffect, useState } from "react";
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
import { AnimatePresence, Reorder } from "framer-motion";
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "src/shared/ui/ui/drawer";
import { ITreeNode } from "src/app/types/nodes";
import { axiosBase } from "src/app/http";
import { useQueryClient } from "react-query";

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
  const queryClient = useQueryClient();
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

  const addNode = async (id: string, type: string) => {
    const { data: newId } = (await postNodes({
      parent: id,
      template_id: type,
    })) as { data: string };
    const newChild: Partial<ITreeNode> = {
      id: newId,
      children: [],
    };
    dispatch(setExistNewChild({ newChild: newChild, id: id }));
    return newId;
  };
  const handleDeleteNode = (id: string) => {
    deleteNodes(id);
    dispatch(deleteNode(id));
  };
  console.log(nodes);

  const [text, setText] = useState("");
  useEffect(() => {
    document.addEventListener("keydown", (e) => {
      if (e.key.length === 1) {
        setText((prev) => prev + e.key);
      }
      if (e.key === "Backspace") {
        setText((prev) => prev.slice(0, -1));
      }
    });
  }, []);
  const renderNode = ({
    id,
    children,
    type_id,
    attrs,
  }: ITreeNode): React.ReactNode => {
    if (isTreeSuccess && tree && id === tree.id) {
      return children?.map((child) => renderNode(child));
    }

    return (
      <Reorder.Item value={id} key={id}>
        <Drawer>
          <div
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
            {type_id === "image" && (
              <img
                src={`http://localhost/api/v1/images/${id}`}
                alt=""
                className="rounded-20"
              />
            )}
            {type_id === "text" && (
              <p className="text-sm break-words relative">{text}</p>
            )}
            {children.length > 0 && (
              <Reorder.Group
                values={children.map((node) => node.id)}
                onReorder={(newOrder: Array<string>) => setNodes(id, newOrder)}
                className={`h-full grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-4`}
              >
                {children.map((child) => renderNode(child))}
              </Reorder.Group>
            )}
            <DrawerTrigger>
              <AddButton />
            </DrawerTrigger>
            <DrawerContent className="bg-white">
              <DrawerHeader>
                <DrawerTitle>Выберите шаблон</DrawerTitle>
              </DrawerHeader>
              <div className="flex flex-col gap-5 py-5 container">
                <div
                  onClick={async () => {
                    addNode(id, templates![2]);
                  }}
                  className="flex justify-between items-center p-3 rounded-20 border"
                >
                  <span className="text-2xl font-bold">Блок</span>
                  <div className="w-20 h-20 bg-black/50 rounded-20" />
                </div>
                <div
                  onClick={async () => {
                    addNode(id, templates![0]);
                  }}
                  className="flex justify-between items-center p-3 rounded-20 border"
                >
                  <span className="text-2xl font-bold">Текст</span>
                  <div className="w-20 h-20 bg-black/50 rounded-20" />
                </div>
                <label
                  htmlFor="image"
                  className="flex justify-between items-center p-3 rounded-20 border"
                >
                  <input
                    type="file"
                    id="image"
                    className="w-0 h-0 absolute"
                    onChange={async (e) => {
                      if (e.target.files) {
                        const formData = new FormData();
                        const newId = await addNode(id, templates![1]);
                        formData.append("file", e.target.files[0]);
                        formData.append("node_id", newId);
                        await axiosBase.post("images/", formData);
                        dispatch(setCoreNewChild({ id: newId, children: [] }));
                        queryClient.invalidateQueries("getTreeNodes");
                      }
                    }}
                  />
                  <span className="text-2xl font-bold">Изображение</span>
                  <div className="w-20 h-20 bg-black/50 rounded-20" />
                </label>
              </div>
            </DrawerContent>
          </div>
        </Drawer>
      </Reorder.Item>
    );
  };

  return (
    <div className="h-fit min-h-screen bg-white p-4">
      <Drawer>
        <AnimatePresence mode="popLayout" initial={false}>
          <Reorder.Group
            values={nodes.children.map((node) => node.id)}
            onReorder={(newOrder: Array<string>) =>
              setNodes(nodes.id, newOrder)
            }
            className="h-full grid grid-rows-[repeat(12, minmax(100px, 1fr))] rows-10 gap-4 "
          >
            {renderNode(nodes as ITreeNode)}
          </Reorder.Group>
        </AnimatePresence>
        <DrawerTrigger className="w-full pt-5">
          <AddButton />
        </DrawerTrigger>
        <DrawerContent className="bg-white">
          <DrawerHeader>
            <DrawerTitle>Выберите шаблон</DrawerTitle>
          </DrawerHeader>
          <div className="flex flex-col gap-5 py-5 container">
            <div
              onClick={async () => {
                const { data: newId } = (await postNodes({
                  parent: tree ? tree.id : "",
                  template_id: templates![2],
                })) as { data: string };
                dispatch(setCoreNewChild({ id: newId, children: [] }));
              }}
              className="flex justify-between items-center p-3 rounded-20 border"
            >
              <span className="text-2xl font-bold">Блок</span>
              <div className="w-20 h-20 bg-black/50 rounded-20" />
            </div>
            <div
              onClick={async () => {
                const { data: newId } = (await postNodes({
                  parent: tree ? tree.id : "",
                  template_id: templates![0],
                })) as { data: string };
                dispatch(setCoreNewChild({ id: newId, children: [] }));
              }}
              className="flex justify-between items-center p-3 rounded-20 border"
            >
              <span className="text-2xl font-bold">Текст</span>
              <div className="w-20 h-20 bg-black/50 rounded-20" />
            </div>
            <label
              htmlFor="image"
              className="flex justify-between items-center p-3 rounded-20 border"
            >
              <input
                onChange={async (e) => {
                  if (e.target.files) {
                    const formData = new FormData();
                    const { data: newId } = (await postNodes({
                      parent: tree ? tree.id : "",
                      template_id: templates![1],
                    })) as { data: string };
                    formData.append("file", e.target.files[0]);
                    formData.append("node_id", newId);
                    await axiosBase.post("images/", formData);
                    dispatch(setCoreNewChild({ id: newId, children: [] }));
                    queryClient.invalidateQueries("getTreeNodes");
                  }
                }}
                type="file"
                id="image"
                className="w-0 h-0 absolute"
              />
              <span className="text-2xl font-bold">Изображение</span>
              <div className="w-20 h-20 bg-black/50 rounded-20" />
            </label>
          </div>
        </DrawerContent>
      </Drawer>
    </div>
  );
};

export default UserPage;
