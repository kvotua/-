export interface INode {
  parent: string;
  id: string;
  type_id: "container" | "text" | "image";
  children: INode[];
  attrs: {
    [key: string]: string;
  };
}

export interface ITreeNode {
  id: string;
  type_id: "container" | "text" | "image";
  attrs: {
    [key: string]: string;
  };
  children: INode[];
}

export interface IPostNode {
  parent: string;
  template_id: string;
}
