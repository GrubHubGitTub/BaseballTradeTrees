import '../styles/globals.css'
import Layout from '../components/Layout.js'
import { useRouter } from 'next/router'

export default function App({ Component, pageProps }) {
  const router = useRouter()
  return (
    <Layout>
      <Component {...pageProps} key={router.asPath} />
    </Layout>
  )
}