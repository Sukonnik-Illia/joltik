import logo from '../assets/images/logo.png';
import React from 'react'

const Navbar = () => {
    return (
        <nav className='bg-indigo-700'>
            <div className='mx-auto max-w-7xl px-2 sm:px-6 lg:px-8'>
                <div className='flex h-20 items-center justify-between'>
                    <div className='flex flex-1 items-center justify-center md:items-stretch md:justify-start'>
                        <img src={logo} alt='logo' className='h-10 w-auto' />
                        Navbar
                    </div>
                </div>
            </div>
        </nav>
    )
};

export default Navbar;
