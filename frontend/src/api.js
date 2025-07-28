import axios from "axios";

const api = axios.create({
  baseURL: "/api/store/",
});

export const getEvents = () =>
  api.get("events/").then((res) => res.data.results);
export const getContents = () =>
  api.get("contents/").then((res) => res.data.results);

export const purchaseEvent = (data) =>
  api.post("purchase/event/", data).then((res) => res.data);
export const purchaseContent = (data) =>
  api.post("purchase/content/", data).then((res) => res.data);
