import { useMutation } from '@apollo/client'

import CREATE_CONTACT_GQL from '../../gql/ai/call/contact/createContact.gql'

interface CreateContactInput {
  name?: string
  agent_id?: string
  team_id?: string
}

export const useCreateContactService = () => {
  const [mutation] = useMutation(CREATE_CONTACT_GQL)

  const createContactService = async (input: any) => {
    // const { name, agent_id, team_id } = input

    const {
      data: { createContact },
    } = await mutation({
      variables: {
        input: {
          name: 'First test',
          description: 'desc',
          group_id: '132306b9-e428-4534-b744-aa8cdf86d1e6',
          email: 'Levanion1998@gmail.com',
          phone: '592444502',
        },
      },
    })

    return createContact
  }

  return [createContactService]
}
