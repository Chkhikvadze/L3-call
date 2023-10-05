import { useMutation } from '@apollo/client'

import CREATE_GROUP_GQL from '../../gql/ai/call/group/createGroup.gql'

interface CreateGroupInput {
  name?: string
  agent_id?: string
  team_id?: string
}

export const useCreateGroupService = () => {
  const [mutation] = useMutation(CREATE_GROUP_GQL)

  const createGroupService = async (input: any) => {
    // const { name, agent_id, team_id } = input

    const {
      data: { createGroup },
    } = await mutation({
      variables: {
        input: {
          name: 'First Group',
          description: 'desc dadadad',
        },
      },
    })

    return createGroup
  }

  return [createGroupService]
}
