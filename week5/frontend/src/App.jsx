import React, { useState, useEffect } from 'react';
import { Menu } from 'antd';
import ReactECharts from 'echarts-for-react';
import axios from 'axios';
import 'antd/dist/reset.css';

function App() {
  const [currentMenu, setCurrentMenu] = useState('ratings');
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchChartData(currentMenu);
  }, [currentMenu]);

  const fetchChartData = async (type) => {
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:5001/api/${type}`);
      setChartData(res.data);
    } catch (error) {
      setChartData(null);
    }
    setLoading(false);
  };

  const getChartOptions = () => {
    if (!chartData) {
      return { title: { text: '暂无数据' } };
    }
    if (currentMenu === 'ratings') {
      return {
        title: { text: '豆瓣电影评分排行榜', left: 'center' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: chartData.titles || [], axisLabel: { rotate: 45, fontSize: 10 } },
        yAxis: { type: 'value', name: '评分' },
        series: [{ type: 'bar', data: chartData.ratings || [], itemStyle: { color: '#1890ff' } }]
      };
    } else if (currentMenu === 'years') {
      return {
        title: { text: '豆瓣电影年份分布', left: 'center' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: chartData.years || [] },
        yAxis: { type: 'value', name: '电影数量' },
        series: [{ type: 'line', data: chartData.counts || [], smooth: true, itemStyle: { color: '#52c41a' } }]
      };
    }
    return {};
  };

  const menuItems = [
    { key: 'ratings', label: ' 评分排行榜' },
    { key: 'years', label: ' 年份分布' }
  ];

  return (
    <div>
      <h1 style={{ padding: '20px 20px 0 20px' }}> 第五周：数据可视化</h1>
      <Menu mode="horizontal" selectedKeys={[currentMenu]} onClick={({ key }) => setCurrentMenu(key)} items={menuItems} />
      <div style={{ padding: 20 }}>
        {loading ? <div style={{ textAlign: 'center', padding: 50 }}>加载中...</div> : <ReactECharts option={getChartOptions()} style={{ height: 500, width: '100%' }} />}
      </div>
    </div>
  );
}

export default App;