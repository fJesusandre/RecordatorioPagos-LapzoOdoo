def generar_correo_usd(nombre, factura, fecha, monto, moneda, dias, url):
    cuerpo_usd = f"""
            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 0; padding: 0; background-color: #f8fafc;">
                <tr>
                    <td align="center" style="padding: 20px 10px;">
                        <!-- Main Container -->
                        <table cellpadding="0" cellspacing="0" border="0" width="640" style="max-width: 640px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); border-radius: 16px; overflow: hidden; font-family: Arial, Helvetica, sans-serif;">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background-color: rgba(255,255,255,0.1); padding: 40px 30px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.2);">
                                    <!-- Logo Container -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin-bottom: 20px;">
                                        <tr>
                                            <td style="background-color: rgba(255,255,255,0.15); padding: 15px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.25);">
                                                <img src="https://i.imgur.com/Bcb5RQK.png" alt="Logo Lapzo" width="48" height="48" style="display: block; border-radius: 12px;">
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Brand Name -->
                                    <h1 style="color: #ffffff; margin: 0 0 15px 0; font-size: 32px; font-weight: bold; letter-spacing: -1px; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">LAPZO</h1>
                                    
                                    <!-- Badge -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center">
                                        <tr>
                                            <td style="background-color: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; border: 1px solid rgba(255,255,255,0.3);">
                                                <p style="color: rgba(255,255,255,0.95); margin: 0; font-size: 14px; font-weight: bold;">🛎 Recordatorio de Pago</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            
                            <!-- Main Content -->
                            <tr>
                                <td style="background-color: #ffffff; padding: 0;">
                                    <!-- Purple Top Border -->
                                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                        <tr>
                                            <td style="height: 4px; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);"></td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Content Padding -->
                                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                        <tr>
                                            <td style="padding: 40px 30px;">
                                                
                                                <!-- Greeting -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 30px;">
                                                    <tr>
                                                        <td>
                                                            <h2 style="color: #1e1b4b; font-size: 24px; font-weight: bold; margin: 0 0 10px 0; letter-spacing: -0.5px;">Hola {nombre} 👋</h2>
                                                            <p style="color: #64748b; font-size: 16px; line-height: 1.5; margin: 0;">¡Se les desea un excelente día!</p><br>
                                                            <p style="color: #64748b; font-size: 16px; line-height: 1.5; margin: 0;">Les recordamos que cuentan con una factura pendiente:</p>
                                                            
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Alert Card -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 25px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; padding: 25px; border: 2px solid #f59e0b;">
                                                            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                <tr>
                                                                    <td width="40" style="vertical-align: top; padding-right: 15px;">
                                                                        <table cellpadding="0" cellspacing="0" border="0">
                                                                            <tr>
                                                                                <td style="width: 40px; height: 40px; background-color: #f59e0b; border-radius: 8px; text-align: center; vertical-align: middle;">
                                                                                    <span style="font-size: 16px;">⚠️</span>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                    <td style="vertical-align: top;">
                                                                        <h3 style="color: #92400e; font-size: 18px; font-weight: bold; margin: 0 0 10px 0;">Factura Pendiente</h3>
                                                                        <p style="color: #92400e; margin: 0; font-size: 15px; line-height: 1.4;">
                                                                            La factura <strong>{factura}</strong> con fecha de vencimiento <strong>{fecha}</strong> aún no ha sido pagada.
                                                                        </p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Amount Card -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 30px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); border-radius: 16px; padding: 35px; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                                                            <p style="color: rgba(255,255,255,0.8); font-size: 14px; margin: 0 0 10px 0; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">Monto Pendiente</p>
                                                            <h2 style="color: #ffffff; font-size: 40px; margin: 0 0 15px 0; font-weight: bold; letter-spacing: -1px;">${monto} {moneda}</h2>
                                                            <table cellpadding="0" cellspacing="0" border="0" align="center">
                                                                <tr>
                                                                    <td style="background-color: rgba(239, 68, 68, 0.2); padding: 8px 16px; border-radius: 25px; border: 1px solid rgba(239, 68, 68, 0.3);">
                                                                        <p style="color: #fecaca; font-size: 13px; margin: 0; font-weight: bold;">🕐 Vencida hace {dias} días</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- CTA Button -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 35px 0;">
                                                    <tr>
                                                        <td align="center">
                                                            <table cellpadding="0" cellspacing="0" border="0">
                                                                <tr>
                                                                    <td style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); border-radius: 25px; border: 1px solid rgba(255,255,255,0.2);">
                                                                        <a href="{url}" target="_blank" style="display: block; padding: 18px 35px; color: #ffffff; text-decoration: none; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">📄 Ver Factura </a>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Message -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 25px 0;">
                                                    <tr>
                                                        <td style="text-align: center;">
                                                            <p style="color: #64748b; font-size: 15px; line-height: 1.5; margin: 0;">Les agradeceríamos procesar este pago lo antes posible.</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Payment Information -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 30px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 16px; padding: 30px; border: 2px solid #8b5cf6;">
                                                            
                                                            <!-- Header -->
                                                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 25px;">
                                                                <tr>
                                                                    <td width="50" style="vertical-align: top; padding-right: 15px;">
                                                                        <table cellpadding="0" cellspacing="0" border="0">
                                                                            <tr>
                                                                                <td style="width: 50px; height: 50px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 12px; text-align: center; vertical-align: middle;">
                                                                                    <span style="font-size: 20px;">🏦</span>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                    <td style="vertical-align: top;">
                                                                        <h3 style="color: #1e1b4b; margin: 0 0 5px 0; font-size: 20px; font-weight: bold;">Información de Pago</h3>
                                                                        <p style="color: #6366f1; margin: 0; font-size: 14px; font-weight: bold;">Transferencia Bancaria Internacional</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            
                                                            <!-- Payment Details -->
                                                            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff; margin-bottom: 10px;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Transfer Method:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px; font-size: 13px;">ACH, WIRE, SWIFT</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Account Number:</td>
                                                                                <td align="right" style="color: #22d3ee; font-family: monospace; background-color: #1e293b; padding: 6px 10px; border-radius: 4px; font-size: 14px; font-weight: bold;">8482026714</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Account Type:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px; font-size: 13px;">Business Checking</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">ACH Routing:</td>
                                                                                <td align="right" style="color: #22d3ee; font-family: monospace; background-color: #1e293b; padding: 6px 10px; border-radius: 4px; font-size: 14px; font-weight: bold;">026073150</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Wire Routing:</td>
                                                                                <td align="right" style="color: #22d3ee; font-family: monospace; background-color: #1e293b; padding: 6px 10px; border-radius: 4px; font-size: 14px; font-weight: bold;">026073008</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px; vertical-align: top;">Beneficiary:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; font-size: 13px; line-height: 1.4; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px;">DECASOL SA de CV<br>Av Frida Kahlo 2222 int1105</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Bank Name:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; font-size: 13px; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px;">Community Federal Savings Bank</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px; vertical-align: top;">Bank Address:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; font-size: 13px; line-height: 1.4; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px;">89-16 Jamaica Ave<br>Woodhaven, NY</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Swift Code:</td>
                                                                                <td align="right" style="color: #22d3ee; font-family: monospace; background-color: #1e293b; padding: 6px 10px; border-radius: 4px; font-size: 14px; font-weight: bold;">CMFGUS33</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Important Notice -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 25px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; padding: 20px; text-align: center; border: 2px solid #f59e0b;">
                                                            <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin-bottom: 12px;">
                                                                <tr>
                                                                    <td style="width: 40px; height: 40px; background-color: #f59e0b; border-radius: 8px; text-align: center; vertical-align: middle;">
                                                                        <span style="font-size: 16px;">💡</span>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <p style="color: #92400e; margin: 0; font-weight: bold; font-size: 15px; line-height: 1.4;">Si ya realizaron la transacción, favor de compartirnos el comprobante de pago.</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Closing Message -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 35px 0 20px 0;">
                                                    <tr>
                                                        <td style="text-align: center;">
                                                            <p style="color: #64748b; font-size: 15px; line-height: 1.5; margin: 0 0 12px 0;">Quedamos atentos para cualquier consulta o aclaración.</p>
                                                            <p style="color: #1e1b4b; font-size: 16px; font-weight: bold; margin: 0;">¡Gracias por su confianza!</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); padding: 30px; text-align: center;">
                                    <!-- Company Name -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin-bottom: 20px;">
                                        <tr>
                                            <td style="background-color: rgba(139, 92, 246, 0.2); padding: 12px 20px; border-radius: 8px; border: 1px solid rgba(139, 92, 246, 0.4);">
                                                <h4 style="color: #ffffff; font-size: 16px; font-weight: bold; margin: 0; letter-spacing: 1px;">DECASOL SA de CV</h4>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Address -->
                                    <p style="color: #ffffff; font-size: 13px; margin: 0 0 15px 0; line-height: 1.4;">
                                        GUSTAVO DÍAZ ORDAZ 3057, Int. 27, CP 64650<br>
                                        MONTERREY, NUEVO LEÓN
                                    </p>
                                    
                                    <!-- WhatsApp -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center">
                                        <tr>
                                            <td style="background-color: rgba(34, 197, 94, 0.2); padding: 10px 20px; border-radius: 25px; border: 1px solid rgba(34, 197, 94, 0.4);">
                                                <p style="color: #70e000; font-size: 13px; margin: 0; font-weight: bold;">
                                                    📞 WhatsApp: <a href="tel:+528135510658" style="color: #ffffff; text-decoration: none; font-weight: bold;">+52 81 3551 0658</a>
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            
                        </table>
                    </td>
                </tr>
            </table>
            """
    return cuerpo_usd

def generar_correo_mxn(nombre, factura, fecha, monto, moneda, dias, url):

    cuerpo_mxn = f"""
            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 0; padding: 0; background-color: #f8fafc;">
                <tr>
                    <td align="center" style="padding: 20px 10px;">
                        <!-- Main Container -->
                        <table cellpadding="0" cellspacing="0" border="0" width="640" style="max-width: 640px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); border-radius: 16px; overflow: hidden; font-family: Arial, Helvetica, sans-serif;">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background-color: rgba(255,255,255,0.1); padding: 40px 30px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.2);">
                                    <!-- Logo Container -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin-bottom: 20px;">
                                        <tr>
                                            <td style="background-color: rgba(255,255,255,0.15); padding: 15px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.25);">
                                                <img src="https://i.imgur.com/Bcb5RQK.png" alt="Logo Lapzo" width="48" height="48" style="display: block; border-radius: 12px;">
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Brand Name -->
                                    <h1 style="color: #ffffff; margin: 0 0 15px 0; font-size: 32px; font-weight: bold; letter-spacing: -1px; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">LAPZO</h1>
                                    
                                    <!-- Badge -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center">
                                        <tr>
                                            <td style="background-color: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 25px; border: 1px solid rgba(255,255,255,0.3);">
                                                <p style="color: rgba(255,255,255,0.95); margin: 0; font-size: 14px; font-weight: bold;">🛎 Recordatorio de Pago</p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            
                            <!-- Main Content -->
                            <tr>
                                <td style="background-color: #ffffff; padding: 0;">
                                    <!-- Purple Top Border -->
                                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                        <tr>
                                            <td style="height: 4px; background: linear-gradient(90deg, #6366f1, #8b5cf6, #a855f7);"></td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Content Padding -->
                                    <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                        <tr>
                                            <td style="padding: 40px 30px;">
                                                
                                                <!-- Greeting -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 30px;">
                                                    <tr>
                                                        <td>
                                                            <h2 style="color: #1e1b4b; font-size: 24px; font-weight: bold; margin: 0 0 10px 0; letter-spacing: -0.5px;">Hola {nombre} 👋</h2>
                                                            <p style="color: #64748b; font-size: 16px; line-height: 1.5; margin: 0;">¡Se les desea un excelente día!</p><br>
                                                            <p style="color: #64748b; font-size: 16px; line-height: 1.5; margin: 0;">Les recordamos que cuentan con una factura pendiente:</p>
                                                            
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Alert Card -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 25px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; padding: 25px; border: 2px solid #f59e0b;">
                                                            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                <tr>
                                                                    <td width="40" style="vertical-align: top; padding-right: 15px;">
                                                                        <table cellpadding="0" cellspacing="0" border="0">
                                                                            <tr>
                                                                                <td style="width: 40px; height: 40px; background-color: #f59e0b; border-radius: 8px; text-align: center; vertical-align: middle;">
                                                                                    <span style="font-size: 16px;">⚠️</span>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                    <td style="vertical-align: top;">
                                                                        <h3 style="color: #92400e; font-size: 18px; font-weight: bold; margin: 0 0 10px 0;">Factura Pendiente</h3>
                                                                        <p style="color: #92400e; margin: 0; font-size: 15px; line-height: 1.4;">
                                                                            La factura <strong>{factura}</strong> con fecha de vencimiento <strong>{fecha}</strong> aún no ha sido pagada.
                                                                        </p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Amount Card -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 30px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); border-radius: 16px; padding: 35px; text-align: center; border: 1px solid rgba(255,255,255,0.2);">
                                                            <p style="color: rgba(255,255,255,0.8); font-size: 14px; margin: 0 0 10px 0; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">Monto Pendiente</p>
                                                            <h2 style="color: #ffffff; font-size: 40px; margin: 0 0 15px 0; font-weight: bold; letter-spacing: -1px;">${monto} {moneda}</h2>
                                                            <table cellpadding="0" cellspacing="0" border="0" align="center">
                                                                <tr>
                                                                    <td style="background-color: rgba(239, 68, 68, 0.2); padding: 8px 16px; border-radius: 25px; border: 1px solid rgba(239, 68, 68, 0.3);">
                                                                        <p style="color: #fecaca; font-size: 13px; margin: 0; font-weight: bold;">🕐 Vencida hace {dias} días</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- CTA Button -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 35px 0;">
                                                    <tr>
                                                        <td align="center">
                                                            <table cellpadding="0" cellspacing="0" border="0">
                                                                <tr>
                                                                    <td style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); border-radius: 25px; border: 1px solid rgba(255,255,255,0.2);">
                                                                        <a href="{url}" target="_blank" style="display: block; padding: 18px 35px; color: #ffffff; text-decoration: none; font-weight: bold; font-size: 16px; letter-spacing: 0.5px;">📄 Ver Factura </a>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Message -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 25px 0;">
                                                    <tr>
                                                        <td style="text-align: center;">
                                                            <p style="color: #64748b; font-size: 15px; line-height: 1.5; margin: 0;">Les agradeceríamos procesar este pago lo antes posible.</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Payment Information -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 30px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); border-radius: 16px; padding: 30px; border: 2px solid #8b5cf6;">
                                                            
                                                            <!-- Header -->
                                                            <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 25px;">
                                                                <tr>
                                                                    <td width="50" style="vertical-align: top; padding-right: 15px;">
                                                                        <table cellpadding="0" cellspacing="0" border="0">
                                                                            <tr>
                                                                                <td style="width: 50px; height: 50px; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 12px; text-align: center; vertical-align: middle;">
                                                                                    <span style="font-size: 20px;">🏦</span>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                    <td style="vertical-align: top;">
                                                                        <h3 style="color: #1e1b4b; margin: 0 0 5px 0; font-size: 20px; font-weight: bold;">Información de Pago</h3>
                                                                        <p style="color: #6366f1; margin: 0; font-size: 14px; font-weight: bold;">Transferencia Bancaria</p>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            
                                                            <!-- Payment Details -->
                                                            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff; margin-bottom: 10px;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Banco:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px; font-size: 13px;">Banamex</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff; margin-bottom: 10px;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Sucursal:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px; font-size: 13px;">861 C F SAN PEDRO NL</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                
                                                                 <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff; margin-bottom: 10px;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Dirección:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px; font-size: 13px;">RIO JORDAN #100 DEL VALLE</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Cuenta de Cheques:</td>
                                                                                <td align="right" style="color: #22d3ee; font-family: monospace; background-color: #1e293b; padding: 6px 10px; border-radius: 4px; font-size: 14px; font-weight: bold;">8012426210</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">CLABE Interbancaria:</td>
                                                                                <td align="right" style="color: #22d3ee; font-family: monospace; background-color: #1e293b; padding: 6px 10px; border-radius: 4px; font-size: 14px; font-weight: bold;">002580700953579529</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                
                                                                
                                                                <tr><td style="height: 8px;"></td></tr>
                                                                <tr>
                                                                    <td style="background-color: #ffffff; border-radius: 8px; padding: 15px; border: 1px solid #e0e7ff;" width="100%">
                                                                        <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                                                            <tr>
                                                                                <td style="color: #1e1b4b; font-weight: bold; font-size: 14px;">Concepto de pago:</td>
                                                                                <td align="right" style="color: #374151; font-weight: bold; font-size: 13px; padding: 4px 8px; background-color: #f1f5f9; border-radius: 4px;">{factura}</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Important Notice -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 25px 0;">
                                                    <tr>
                                                        <td style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; padding: 20px; text-align: center; border: 2px solid #f59e0b;">
                                                            <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin-bottom: 12px;">
                                                                <tr>
                                                                    <td style="width: 40px; height: 40px; background-color: #f59e0b; border-radius: 8px; text-align: center; vertical-align: middle;">
                                                                        <span style="font-size: 16px;">💡</span>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                            <p style="color: #92400e; margin: 0; font-weight: bold; font-size: 15px; line-height: 1.4;">Si ya realizaron la transacción, favor de compartirnos el comprobante de pago.</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                                <!-- Closing Message -->
                                                <table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin: 35px 0 20px 0;">
                                                    <tr>
                                                        <td style="text-align: center;">
                                                            <p style="color: #64748b; font-size: 15px; line-height: 1.5; margin: 0 0 12px 0;">Quedamos atentos para cualquier consulta o aclaración.</p>
                                                            <p style="color: #1e1b4b; font-size: 16px; font-weight: bold; margin: 0;">¡Gracias por su confianza!</p>
                                                        </td>
                                                    </tr>
                                                </table>
                                                
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            
                            <!-- Footer -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%); padding: 30px; text-align: center;">
                                    <!-- Company Name -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center" style="margin-bottom: 20px;">
                                        <tr>
                                            <td style="background-color: rgba(139, 92, 246, 0.2); padding: 12px 20px; border-radius: 8px; border: 1px solid rgba(139, 92, 246, 0.4);">
                                                <h4 style="color: #ffffff; font-size: 16px; font-weight: bold; margin: 0; letter-spacing: 1px;">DECASOL SA de CV</h4>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <!-- Address -->
                                    <p style="color: #ffffff; font-size: 13px; margin: 0 0 15px 0; line-height: 1.4;">
                                        GUSTAVO DÍAZ ORDAZ 3057, Int. 27, CP 64650<br>
                                        MONTERREY, NUEVO LEÓN
                                    </p>
                                    
                                    <!-- WhatsApp -->
                                    <table cellpadding="0" cellspacing="0" border="0" align="center">
                                        <tr>
                                            <td style="background-color: rgba(34, 197, 94, 0.2); padding: 10px 20px; border-radius: 25px; border: 1px solid rgba(34, 197, 94, 0.4);">
                                                <p style="color: #70e000; font-size: 13px; margin: 0; font-weight: bold;">
                                                    📞 WhatsApp: <a href="tel:+528135510658" style="color: #ffffff; text-decoration: none; font-weight: bold;">+52 81 3551 0658</a>
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            
                        </table>
                    </td>
                </tr>
            </table>
            """
    return cuerpo_mxn

