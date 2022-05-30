import React from "react";
import axios from "axios";

export default function GetCameraFeedId(props) {
  const baseURL =
    "https://6r8fhtwkwj.execute-api.us-west-2.amazonaws.com/development/enrichedframe";
  const [post, setPost] = React.useState(null);
  const headers = {
    "X-api-key": "zTkcZF8YHM6dqoFGLuQky3c9oTWBnjTmaZ2ZdjtF",
  };
  React.useEffect(() => {
      axios.get(baseURL, { headers }).then((response) => {
        const result = response.data;
        const filtered = result.filter((a) => a.cameraId == props.id);
        setPost(filtered);
        console.log(filtered);});
  }, []);
  React.useEffect(() => {
    const interval = setInterval(() => {
      console.log('This will run every second!');
      axios.get(baseURL, { headers }).then((response) => {
        const result = response.data;
        const filtered = result.filter((a) => a.cameraId == props.id);
        setPost(filtered);
        console.log(filtered);});
    }, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div>Camera: {props.id}</div>
      {/* {JSON.stringify(post[0]?.s3_presigned_url)} */}
     { post &&<img
        src={`${post[0]?.s3_presigned_url}`}
        alt="camera"
        width="100%"
      />}
    </div>
  );
}
