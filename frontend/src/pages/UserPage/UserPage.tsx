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
  updateNode,
} from "src/app/store/slice/UserPgaeSlice";
import {
  useDeleteNodesMutation,
  useLazyGetNodesQuery,
  usePatchAttrMutation,
  usePostNodesMutation,
} from "src/app/store/slice/UserPgaeSlice/UserPageApi";
import { AddButton } from "src/shared/AddButton/AddButton";
import Back from "src/app/assets/icons/back.svg?react";
import Trash from "src/app/assets/icons/trash.svg?react";
import Return from "src/app/assets/icons/return.svg?react";
import Exit from "src/app/assets/icons/exit.svg?react";
import Edit from "src/app/assets/icons/edit.svg?react";
import { useNavigate, useParams } from "react-router-dom";
import { menuContext } from "src/app/context";
import { AnimatePresence, Reorder, ValueTarget, motion } from "framer-motion";
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
import { InputDefault } from "src/shared/InputDefault/InputDefault";
import { LinkButton } from "src/shared/LinkButton/LinkButton";
import Alignment from "src/widgets/Alignment/Alignment";

const UserPage: React.FC = () => {
  const [align, setAlign] = useState<string>("text-left");
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { projectId } = useParams();
  const nodes = useAppSelector((state) => state.userPage);
  const setNodes = (node_id: string, new_nodes: Array<string>) =>
    dispatch(setChildrens({ id: node_id, children: new_nodes }));
  const { tree, isTreeSuccess, templates, getIdByType } = useGetTree<ITreeNode>(
    projectId!,
  );
  console.log(templates);

  const { setMenuItems } = useContext(menuContext);
  const [deleteNodes] = useDeleteNodesMutation();
  const queryClient = useQueryClient();
  const [selectedType, setSelectedType] = useState<
    "container" | "text" | "image" | null
  >(null);
  const [animate, setAnimate] = useState(false);
  const [nodeText, setNodeText] = useState<string>("");

  interface IAttribute {
    node_id: string;
    attribute_name: string;
    attribute_value: string;
  }

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
  const [getNodes] = useLazyGetNodesQuery();
  const [patchAttr] = usePatchAttrMutation();
  const addNode = async (id: string, type: string) => {
    const { data: newId } = (await postNodes({
      parent: id,
      template_id: type,
    })) as { data: string };
    const { data } = await getNodes(newId);
    console.log(data);

    const newChild: Partial<ITreeNode> = {
      id: newId,
      attrs: data.attrs,
      type_id: data.type_id,
      children: [],
    };
    dispatch(setExistNewChild({ newChild: newChild, id: id }));
    return newId;
  };
  const patchNode = async (attribute: IAttribute) => {
    await patchAttr(attribute);
    const { data } = await getNodes(attribute.node_id);
    const newChild = {
      attrs: await data.attrs,
      type_id: await data.type_id,
      children: [],
    };
    dispatch(updateNode({ id: attribute.node_id, updatedValues: newChild }));
  };
  const handleDeleteNode = (id: string) => {
    deleteNodes(id);
    dispatch(deleteNode(id));
  };
  console.log(nodes);

  const [activeItem, setActiveItem] = useState(false);
  const [activeItemChoice, setActiveItemChoice] = useState("");
  type Tevent = {
    target: {
      elements: {
        color: {
          value: string;
        };
      };
    };
  };
  const handleSubmit = async (
    event: SubmitEvent | Tevent | React.FormEvent<HTMLFormElement>,
    id: string,
  ) => {
    const submitEvent: SubmitEvent = event as SubmitEvent;
    const targetEvent: Tevent = event as Tevent;
    submitEvent.preventDefault();

    const color = targetEvent.target.elements.color.value;

    console.log(color);

    const newId = await addNode(id, getIdByType("text"));
    const text = {
      node_id: newId,
      attribute_name: "text",
      attribute_value: nodeText,
    };
    await patchNode(text);
    const position = {
      node_id: newId,
      attribute_name: "position",
      attribute_value: align,
    };
    await patchNode(position);
    const colorAttr = {
      node_id: newId,
      attribute_name: "color",
      attribute_value: color,
    };
    await patchNode(colorAttr);
  };

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
      <Reorder.Item dragListener={activeItem} value={id} key={id}>
        <Drawer>
          <div
            onClick={(event) => {
              if (event.target === event.currentTarget) {
                setActiveItemChoice(id);
                setActiveItem(true);
                setMenuItems([
                  {
                    handleClick: () => {
                      setActiveItem(false);
                      setActiveItemChoice("");
                      setBaseMenu();
                    },
                    Image: Back,
                  },
                  {
                    handleClick: () => {
                      setBaseMenu();
                    },
                    Image: Edit,
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
            className={`px-4 py-8 border-2 border-black w-full grid text-4xl gap-4 rounded-20 ${activeItemChoice === id ? "shake" : ""}`}
          >
            {type_id === "image" && (
              <img
                src={`http://localhost/api/v1/images/${id}`}
                alt=""
                className="rounded-20"
              />
            )}
            {type_id === "text" && (
              <p
                className={`text-sm break-words relative ${attrs.position}`}
                style={{ color: attrs.color }}
              >
                {attrs.text}
              </p>
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
            <DrawerTrigger
              onClick={() => {
                setAnimate(false);
                setSelectedType(null);
              }}
            >
              <AddButton />
            </DrawerTrigger>
            <DrawerContent className="bg-white">
              {selectedType === null && (
                <motion.div
                  key="visible"
                  initial={animate ? { x: "-100%" } : false}
                  animate={{ x: 0 }}
                  exit={{ x: "-100%" }}
                  transition={{ duration: 0.2 }}
                  className=" w-full"
                >
                  <DrawerHeader>
                    <DrawerTitle>Выберите шаблон</DrawerTitle>
                  </DrawerHeader>
                  <div className="flex flex-col gap-5 py-5 container">
                    <div
                      onClick={async () => {
                        setAnimate(true);
                        setSelectedType("container");
                      }}
                      className="flex justify-between items-center p-3 rounded-20 border"
                    >
                      <span className="text-2xl font-bold">Блок</span>
                      <div className="w-20 h-20 bg-black/50 rounded-20" />
                    </div>
                    <div
                      onClick={() => {
                        setAnimate(true);
                        setSelectedType("text");
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
                            dispatch(
                              setCoreNewChild({ id: newId, children: [] }),
                            );
                            queryClient.invalidateQueries("getTreeNodes");
                          }
                        }}
                      />
                      <span className="text-2xl font-bold">Изображение</span>
                      <div className="w-20 h-20 bg-black/50 rounded-20" />
                    </label>
                  </div>
                </motion.div>
              )}
              {selectedType === "text" && (
                <motion.div
                  key="hidden"
                  initial={{ x: "100%" }}
                  animate={{ x: 0 }}
                  exit={{ x: "100%" }}
                  transition={{ duration: 0.2 }}
                  // className="absolute bottom-0 bg-white w-full"
                >
                  <DrawerHeader className="flex justify-between items-center">
                    <Return
                      onClick={() => {
                        setAnimate(true);
                        setSelectedType(null);
                      }}
                    />
                    <DrawerTitle className="mx-auto">Текст</DrawerTitle>
                  </DrawerHeader>
                  <form
                    onSubmit={(e) => handleSubmit(e, id)}
                    className="flex flex-col gap-5 py-5 container "
                  >
                    <Alignment align={align} setAlign={setAlign} />
                    <InputDefault
                      type="text"
                      name="nodeText"
                      handleChange={setNodeText}
                      valueInp={nodeText}
                      placeholder="Введите текст"
                      className="placeholder:text-mainBlack text-mainBlack"
                    />
                    <input id="color" name="color" type="color" />
                    <DrawerTrigger>
                      <LinkButton
                        title="Сохранить"
                        buttonActive={nodeText === "" ? true : false}
                        type="submit"
                      />
                    </DrawerTrigger>
                  </form>
                </motion.div>
              )}
              {selectedType === "container" && (
                <motion.div
                  key="hidden"
                  initial={{ x: "100%" }}
                  animate={{ x: 0 }}
                  exit={{ x: "100%" }}
                  transition={{ duration: 0.2 }}
                  // className="absolute bottom-0 bg-white w-full"
                >
                  <DrawerHeader className="flex justify-between items-center">
                    <Return
                      onClick={() => {
                        setAnimate(true);
                        setSelectedType(null);
                      }}
                    />
                    <DrawerTitle className="mx-auto">Блок</DrawerTitle>
                  </DrawerHeader>
                  <div className="flex flex-col gap-5 py-5 container ">
                    <DrawerTrigger>
                      <LinkButton
                        type=""
                        handleClick={async () => {
                          const newId = await addNode(
                            id,
                            getIdByType("container"),
                          );
                          // const attribute = {
                          //   node_id: newId,
                          //   attribute_name: "text",
                          //   attribute_value: nodeText,
                          // };
                          // await patchNode(attribute);
                        }}
                        title="Сохранить"
                        buttonActive={nodeText === "" ? true : false}
                      />
                    </DrawerTrigger>
                  </div>
                </motion.div>
              )}
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
          <motion.div>
            <DrawerHeader>
              <DrawerTitle>Выберите шаблон</DrawerTitle>
            </DrawerHeader>
            <div className="flex flex-col gap-5 py-5 container">
              <div
                onClick={async () => {
                  const { data: newId } = (await postNodes({
                    parent: tree ? tree.id : "",
                    template_id: getIdByType("container"),
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
          </motion.div>
        </DrawerContent>
      </Drawer>
    </div>
  );
};

export default UserPage;
