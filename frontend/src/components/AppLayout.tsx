"use client"

import * as React from "react"

import { cn } from "@/lib/utils"
// import { Icons } from "@/components/icons"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"
import png from '../assets/fullstack.png'

function Navigation() {
  return (
    <NavigationMenu className="p-4 shadow-xl w-full max-w-full">
      <NavigationMenuList>
        <NavigationMenuItem>
          <NavigationMenuTrigger>Starta här</NavigationMenuTrigger>
          <NavigationMenuContent>
            <ul className="grid gap-3 p-4 md:w-[400px] lg:w-[500px] lg:grid-cols-[.75fr_1fr]">
              <li className="row-span-3">
                <NavigationMenuLink asChild>
                  <a
                    className="flex h-full w-full select-none flex-col justify-end rounded-md bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md"
                    href="/"
                  >
                    <img src={png} alt="" className="w-30 h-30" />
                    <div className="mb-2 mt-4 text-lg font-medium">
                      JobForge
                    </div>
                    <p className="text-sm leading-tight text-muted-foreground">
                      Underlättar dina jobbansökningar
                    </p>
                  </a>
                </NavigationMenuLink>
              </li>
              <ListItem href="/home" title="Smart AI">
                Specialiserad AI på just jobbannonser.
              </ListItem>
              <ListItem href="/home" title="Relevant data">
                Baserad på historisk data.
              </ListItem>
              <ListItem href="/home" title="Effektiv">
                Snabb och smidigt
              </ListItem> 
            </ul>
          </NavigationMenuContent>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <a href="/home" >
            <NavigationMenuLink className={navigationMenuTriggerStyle()}>
              Dokumentation
            </NavigationMenuLink>
          </a>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  )
}

const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          ref={ref}
          className={cn(
            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            className
          )}
          {...props}
        >
          <div className="text-sm font-medium leading-none">{title}</div>
          <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  )
})
ListItem.displayName = "ListItem"

export default function AppLayout({
	children,
}: {
	children: React.ReactNode
}) {
	return (
		<div className="flex flex-col min-h-screen">
			<nav className="flex w-full items-center bg-gray-700">
				<Navigation />
			</nav>
			<main className="flex-grow bg-gray-600 w-full">
				{children}
			</main>
			<footer className="mt-auto w-full bg-gray-700 border-t-2 border-foreground/10 ml-2">
				<div className="flex justify-between p-6">
					<p className="text-lg text-white">JobForge &copy;</p>
					<p className="text-lg text-white">Förenklar ditt personliga brev</p>
				</div>
				<div>
					<ul className="flex justify-between px-6 pb-5">
						<li className="hover:text-gray-400 text-white">
							<a href="/app/course" className="text-white">Start</a>
						</li>
						<li className="hover:text-gray-400 text-white">Dokumentation</li>
						<li className="hover:text-gray-400 text-white">Varför JobForge?</li>
						<li className="hover:text-gray-400 text-white">
							<a href="/app/review" className="text-white">Om oss</a>
						</li>
					</ul>
				</div>
			</footer>
		</div>
	);
}