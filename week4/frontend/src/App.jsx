import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [getInput, setGetInput] = useState('');
  const [postBodyInput, setPostBodyInput] = useState('');
  const [postParamInput, setPostParamInput] = useState('');
  const [response, setResponse] = useState('');

  const handleGet = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/api/get?params=${getInput}`);
      setResponse(res.data.message);
    } catch (error) {
      setResponse('请求失败，请检查后端');
    }
  };

  const handlePost = async () => {
    try {
      const res = await axios.post(
        `http://localhost:5000/api/post?param_params=${postParamInput}`,
        { body_params: postBodyInput }
      );
      setResponse(res.data.message);
    } catch (error) {
      setResponse('请求失败，请检查后端');
    }
  };

  return (
    <div style={{ padding: 40, fontFamily: 'Arial' }}>
      <h1>第四周 - 前后端联调</h1>
      <hr />
      <div>
        <label>输入框1 (GET参数): </label>
        <input onChange={(e) => setGetInput(e.target.value)} style={{ width: 200, padding: 5 }} />
      </div>
      <div>
        <label>输入框2 (POST body): </label>
        <input onChange={(e) => setPostBodyInput(e.target.value)} style={{ width: 200, padding: 5 }} />
      </div>
      <div>
        <label>输入框3 (POST param): </label>
        <input onChange={(e) => setPostParamInput(e.target.value)} style={{ width: 200, padding: 5 }} />
      </div>
      <br />
      <button onClick={handleGet} style={{ padding: '8px 20px', marginRight: 10 }}>按钮1: GET请求</button>
      <button onClick={handlePost} style={{ padding: '8px 20px' }}>按钮2: POST请求</button>
      <h3>后端返回: {response}</h3>
    </div>
  );
}

export default App;