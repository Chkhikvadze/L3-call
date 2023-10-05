import { useMutation } from '@apollo/client'
import { truncate } from 'lodash/fp'

import CREATE_SCHEDULE_GQL from '../../gql/ai/call/schedule/createSchedule.gql'

interface CreateScheduleInput {
  name: string
  description: string
}

export const useCreateScheduleService = () => {
  const [mutation] = useMutation(CREATE_SCHEDULE_GQL)

  const createScheduleService = async (input: any) => {
    // const { name, description } = input

    const {
      data: { createSchedule },
    } = await mutation({
      variables: {
        input: {
          schedule: {
            is_active: truncate,
            name: '',
            schedule_type: 'Agent Type 1',
            description: '',
            max_daily_budget: 0.1,
            cron_expression: 'cron expression',
          },
          configs: {
            agent_id: '0ae8ff52-9b94-4e42-a07e-dfa0e9f4500e',
            group_id: 'd87e6ede-9993-438c-8085-d5f00f09a51c',
          },
        },
      },
    })

    return createSchedule
  }

  return [createScheduleService]
}
