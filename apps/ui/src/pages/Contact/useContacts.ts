import { useContactsService } from 'services/contact/useContactsService'

export const useContacts = () => {
  const { data: contacts } = useContactsService()

  return {
    contacts,
  }
}
