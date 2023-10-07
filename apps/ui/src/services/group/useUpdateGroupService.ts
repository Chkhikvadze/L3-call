import { useMutation } from '@apollo/client'
import UPDATE_CONTACT_GQL from '../../gql/ai/call/contact/updateContact.gql'
import { GroupInput } from './useCreateGroupService'

export const useUpdateGroupService = () => {
  const [mutation] = useMutation(UPDATE_CONTACT_GQL)
  const updateGroup = async (id: string, input: GroupInput) => {
    const { name, description } = input

    const { data } = await mutation({
      variables: {
        id,
        input: {
          name,
          description,
        },
      },
    })
    return data
  }

  return [updateGroup]
}
