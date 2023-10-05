import { useGroupsService } from 'services/group/useGroupsService'

import { ToastContext } from 'contexts'
import { useModal } from 'hooks'
import { useContext } from 'react'

export const useGroups = () => {
  const { setToast } = useContext(ToastContext)
  const { openModal, closeModal } = useModal()

  const { data: groups } = useGroupsService()

  return {
    groups,
  }
}
