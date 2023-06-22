import { Inter } from 'next/font/google';
import './globals.css';

/**
 * Font for the entire page.
 */
const inter = Inter({ subsets: ['latin'] });

/**
 * Metadata about the site.
 */
export const metadata = {
	title: 'Create Next App',
	description: 'Generated by create next app',
};

/**
 * The root layout of the site.
 */
export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html lang='en'>
			<body className={inter.className}>
				<div id='tip'></div>
				{children}
			</body>
		</html>
	);
}
