import { useCreateContactService } from 'services/contact/useCreateContact'

const Contacts = () => {
  const [createContactService] = useCreateContactService()

  return (
    <>
      <span>Contacts page</span>
      <button onClick={() => createContactService('dadad')}> Create Contact</button>
    </>
  )
}

export default Contacts
