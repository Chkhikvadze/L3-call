import { useQuery } from '@apollo/client'
import groupsGql from '../../gql/ai/call/group/groups.gql'

export const useGroupsService = () => {
  const { data, error, loading, refetch } = useQuery(groupsGql)

  return {
    data: data?.getGroups || [],
    error,
    loading,
    refetch,
  }
}
