import Link from 'next/link'

export default function UnauthorizedPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 dark:bg-zinc-900 px-4 text-center">
      <h1 className="text-6xl font-black text-gray-900 dark:text-white">403</h1>
      <h2 className="mt-4 text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
        Acesso Negado
      </h2>
      <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
        Você não tem permissão para acessar esta página.
      </p>
      <div className="mt-8 flex gap-4">
        <Link
          href="/"
          className="rounded-md bg-gray-600 px-4 py-2 text-white hover:bg-gray-700 transition-colors"
        >
          Voltar ao Início
        </Link>
        <Link
          href="/login"
          className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 transition-colors"
        >
          Fazer Login com outra conta
        </Link>
      </div>
    </div>
  )
}
