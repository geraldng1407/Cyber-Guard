import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  PopoverGroup,
} from '@headlessui/react'
import {
  ArrowPathIcon,
  Bars3Icon,
  ChartPieIcon,
  CursorArrowRaysIcon,
  FingerPrintIcon,
  SquaresPlusIcon,
} from '@heroicons/react/24/outline'
import { PhoneIcon, PlayCircleIcon } from '@heroicons/react/20/solid'

const products = [
  { name: 'Analytics', description: 'Get a better understanding of your traffic', href: '#', icon: ChartPieIcon },
  { name: 'Engagement', description: 'Speak directly to your customers', href: '#', icon: CursorArrowRaysIcon },
  { name: 'Security', description: 'Your customers’ data will be safe and secure', href: '#', icon: FingerPrintIcon },
  { name: 'Integrations', description: 'Connect with third-party tools', href: '#', icon: SquaresPlusIcon },
  { name: 'Automations', description: 'Build strategic funnels that will convert', href: '#', icon: ArrowPathIcon },
]
const callsToAction = [
  { name: 'Watch demo', href: '#', icon: PlayCircleIcon },
  { name: 'Contact sales', href: '#', icon: PhoneIcon },
]

const NavBar = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="bg-[#000230]">
      <nav aria-label="Global" className="mx-auto flex w-full items-center justify-between p-6 lg:px-8">
        <div className="flex lg:flex-1">
          <div className=" lg:flex lg:flex-1 lg:justify-start">
            
            <span className="pl-8 py-4 font-orbitron font-bold text-5xl leading-6 text-white">CyberGuard</span>
          </div>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            onClick={() => setMobileMenuOpen(true)}
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700"
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon aria-hidden="true" className="h-6 w-6" />
          </button>
        </div>
        <PopoverGroup className="hidden lg:flex lg:gap-x-12">
          <Link to="/" className="text-lg font-semibold leading-6 text-[#A7BBFF]">
            Home
          </Link>

          <Link to="/applicationsmain" className="text-lg font-semibold leading-6 text-[#A7BBFF]">
            Applications
          </Link>
          <Link to="/countriesmain" className="text-lg font-semibold leading-6 text-[#A7BBFF]">
            Countries
          </Link>
          <Link to="/alerts/history" className="text-lg font-semibold leading-6 text-[#A7BBFF]">
            Alerts
          </Link>
          <Link to="/settings" className="text-lg font-semibold leading-6 text-[#A7BBFF]">
            Settings
          </Link>
        </PopoverGroup>
        <div className="hidden lg:flex lg:flex-1 lg:justify-end">
          <a href="#" className="text-lg font-semibold leading-6 text-white">
            Log in <span aria-hidden="true">&rarr;</span>
          </a>
        </div>
      </nav>
    </header>
  )
}

export default NavBar;