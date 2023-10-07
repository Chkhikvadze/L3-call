import { ToastContext } from 'contexts'
import { useFormik } from 'formik'

import { useContext, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAgentByIdService } from 'services/agent/useAgentByIdService'
import { useUpdateAgentService } from 'services/agent/useUpdateAgentService'
import { agentValidationSchema } from 'utils/validationsSchema'

export const useEditContact = () => {
  const navigate = useNavigate()
  const params = useParams()

  const { contactId } = params

  return {}
}
