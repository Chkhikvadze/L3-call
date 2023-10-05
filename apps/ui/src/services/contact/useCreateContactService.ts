import { useMutation } from '@apollo/client'

import CREATE_CONTACT_GQL from '../../gql/ai/call/contact/createContact.gql'

interface CreateContactInput {
  name: string
  description: string
  group_id: string
  email: string
  phone: string
}

export const useCreateContactService = () => {
  const [mutation] = useMutation(CREATE_CONTACT_GQL)

  const createContactService = async (input: CreateContactInput) => {
    const { name, description, group_id, email, phone } = input

    const {
      data: { createContact },
    } = await mutation({
      variables: {
        input: {
          name,
          description,
          group_id,
          email,
          phone,
        },
      },
    })

    return createContact
  }

  return [createContactService]
}
