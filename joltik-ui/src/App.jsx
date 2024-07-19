import React from 'react'
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import HomeCards from './components/HomeCards';


var h_title = "Customers";
var h_subtitle = "Manage your customers with ease."


const App = () => {
  return (
    <>
      <Navbar />
      <Hero title={h_title} subtitle={h_subtitle} />
      <HomeCards />
      <div className="text-5xl">App</div>
    </>
  )
}

export default App
