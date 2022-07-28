import { useRouter } from 'next/router'

const PlayerPage = () => {
  const router = useRouter()
  const { pid } = router.query

  return <p>PlayerPage: {pid}</p>
}

export default PlayerPage
